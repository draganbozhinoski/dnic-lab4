from django.contrib import admin
from .models import CustomUser, BlogPost, Blocked, BlogPostComment
from django.contrib.auth.models import User
from rangefilter.filters import DateRangeFilter


# from django.contrib.auth.hashers import make_password


# Register your models here.

# admin.site.unregister(User)
#
#
# class ChangeUserAdmin(admin.ModelAdmin):
#     list_display = ('username',)
#
#     def has_change_permission(self, request, obj=None):
#         if obj and obj == request.user:
#             return True
#         return False
#
#     def get_fields(self, request, obj=None):
#         fields = list(super().get_fields(request, obj))
#         print(fields)
#         if request.user.username == 'admin':
#             return fields
#         else:
#             fields.remove('is_superuser')
#             fields.remove('user_permissions')
#             return fields
#
#
# admin.site.register(User, ChangeUserAdmin)
#

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('user',)

    def has_change_permission(self, request, obj=None):
        if obj and obj.user == request.user:
            return True
        return False


admin.site.register(CustomUser, CustomUserAdmin)


class BlogPostCommentAdminInline(admin.StackedInline):
    exclude = ('comment_writer',)
    model = BlogPostComment
    extra = 0


class BlogPostCommentAdmin(admin.ModelAdmin):  # napraven e model za da moze da si ima posebni permisii
    # za dodavanje na komentar na drugi postovi.
    exclude = ('comment_writer',)
    list_display = ('comment_writer', 'sodrzhina')

    def has_add_permission(self, request):
        if CustomUser.objects.filter(user=request.user):
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if obj and (obj.comment_writer.user == request.user or obj.post.writer.user == request.user):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if obj and obj.comment_writer.user == request.user:
            return True
        return False

    def save_model(self, request, obj, form, change):
        blog_user = CustomUser.objects.get(user=request.user)
        if blog_user:
            obj.comment_writer = blog_user
        super().save_model(request, obj, form, change)


admin.site.register(BlogPostComment, BlogPostCommentAdmin)


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'writer')
    exclude = ('writer',)
    search_fields = ('title', 'content')
    list_filter = (('date_created', DateRangeFilter),)
    inlines = [BlogPostCommentAdminInline, ]

    def save_model(self, request, obj, form, change):
        blog_user = CustomUser.objects.get(user=request.user)
        if blog_user:
            obj.writer = blog_user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if obj and obj.writer.user == request.user or request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if obj and obj.writer.user == request.user or request.user.is_superuser:
            return True
        return False

    def has_view_permission(self, request, obj=None):
        if obj:
            if Blocked.objects.filter(
                    user_blocker=obj.writer,
                    user_blocked=CustomUser.objects.filter(user=request.user).first()):
                return False
            return True
        return True

    def has_add_permission(self, request):
        if CustomUser.objects.filter(user=request.user):
            return True
        return False

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.comment_writer = CustomUser.objects.filter(user=request.user).first()
        formset.save_m2m()
        super().save_formset(request, form, formset, change)


admin.site.register(BlogPost, BlogPostAdmin)


class BlockedAdmin(admin.ModelAdmin):
    list_display = ('user_blocker', 'user_blocked')
    exclude = ('user_blocker',)

    def save_model(self, request, obj, form, change):
        blocker = CustomUser.objects.get(user=request.user)
        obj.user_blocker = blocker
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        if CustomUser.objects.filter(user=request.user):
            return True
        return False


admin.site.register(Blocked, BlockedAdmin)
