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


class BlogPostCommentAdmin(admin.StackedInline):
    model = BlogPostComment
    extra = 0
    def has_change_permission(self, request, obj=None):
        return True
    def has_add_permission(self, request, obj):
        return True


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'writer')
    exclude = ('writer',)
    search_fields = ('title', 'content')
    list_filter = (('date_created', DateRangeFilter),)
    inlines = [BlogPostCommentAdmin, ]

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
                    user_blocker=obj.writer.user,
                    user_blocked=request.user):
                return False
            return True
        return True

    # TODO:So custom userite da se izmeni ^

    def has_add_permission(self, request):
        if CustomUser.objects.filter(user=request.user):
            return True
        return False


admin.site.register(BlogPost, BlogPostAdmin)


class BlockedAdmin(admin.ModelAdmin):
    list_display = ('user_blocker', 'user_blocked')
    exclude = ('user_blocker',)

    def save_model(self, request, obj, form, change):
        blocker = User.objects.get(username=request.user.username)
        obj.user_blocker = blocker
        super().save_model(request, obj, form, change)


admin.site.register(Blocked, BlockedAdmin)
