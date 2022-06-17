from django.shortcuts import render, redirect
from .models import BlogPost, Blocked, CustomUser
from .forms import AddBlockedForm, AddPostsForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return redirect('posts')


def posts(request):
    request_custom_user = CustomUser.objects.filter(user=request.user).first()
    users_in_block = Blocked.objects.filter(Q(user_blocker=request_custom_user) | Q(user_blocked=request_custom_user))
    list_users = []
    for user in users_in_block:
        list_users.append(user.user_blocker)
        list_users.append(user.user_blocked)
    set_users = set(list_users)
    set_users.add(request_custom_user)
    posts_list = BlogPost.objects.exclude(writer__in=set_users)
    context = {'posts': posts_list}
    return render(request, 'posts.html', context=context)


def add_post(request):
    if request.method == 'POST':
        form_data = AddPostsForm(request.POST, files=request.FILES)
        print(form_data.is_valid())
        if form_data.is_valid():
            post = form_data.save(commit=False)
            post.writer = CustomUser.objects.filter(user=request.user).first()
            post.save()
            return redirect('posts')
    context = {'form': AddPostsForm}
    return render(request, 'add_post.html', context=context)


@login_required(login_url='/admin/')
def profile(request):
    user = CustomUser.objects.filter(user=request.user).first()
    error = None
    if not user:
        error = "Error happened: User is not Blog User!"
    if error:
        context = {'user': user, 'error': error}
    else:
        posts = BlogPost.objects.filter(writer=user).all()
        context = {'user': user, 'posts': posts}
    return render(request, 'profile.html', context=context)


def blockedUsers(request):
    if request.method == 'POST':
        form_data = AddBlockedForm(request.POST)
        if form_data.is_valid():
            blocked = form_data.save(commit=False)
            blocked.user_blocker = CustomUser.objects.filter(user=request.user).first()
            blocked.save()
            return redirect('blockedUsers')
    custom_user = CustomUser.objects.filter(user=request.user).first()
    blocked_users = Blocked.objects.filter(user_blocker=custom_user)
    context = {'form': AddBlockedForm, 'blocked_users': blocked_users}
    return render(request, 'blocked_users.html', context=context)
