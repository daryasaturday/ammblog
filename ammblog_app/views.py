from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth.models import User
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from ammblog_app.forms import AuthenticateForm, UserCreateForm, BlogPostForm
from ammblog_app.models import BlogPost

def index(request):
    # User is logged in
    if request.user.is_authenticated():
        blogpost_form = BlogPostForm(data=request.POST) if request.method == 'POST' else BlogPostForm()
        user = request.user
        posts_self = BlogPost.objects.filter(user=user.id).order_by('-creation_date')
        posts_buddies = BlogPost.objects.filter(user__userprofile__in=user.profile.follows.all)
        blogPosts = posts_self | posts_buddies

        return render(request,
                      'buddies.html',
                      {'blogpost_form': blogpost_form, 'user': user,
                       'blogPosts': blogPosts,
                       'next_url': '/', })
    else:
        # User is not logged in
        auth_form = AuthenticateForm(data=request.POST) if request.method == 'POST' else AuthenticateForm()

        return render(request,
                      'home.html',
                      {'auth_form': auth_form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # Success
            return redirect(request.path)
        else:
            # Failure
            return index(request)
    return redirect('/')


def logout_view(request):
    logout(request)
    return redirect('/')


def signup(request):
    user_form = UserCreateForm(data=request.POST)
    if request.method == 'POST':
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password2']
            user_form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    return register(request, user_form=user_form)


def register(request, user_form=None):
    form = user_form or UserCreateForm()
    return render(request, 'register.html', {'user_form': form})

@login_required
def submit(request):
    if request.method == "POST":
        post_form = BlogPostForm(data=request.POST)
        next_url = request.POST.get("next_url", "/")
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect(next_url)
        else:
            return index(request)
    return redirect('/')


def get_latest(user):
    try:
        return user.blogpost_set.latest('id')
    except ObjectDoesNotExist:
        return ""


@login_required
def users(request, username=""):
    if username:
        # Show a profile
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
        posts = BlogPost.objects.filter(user=user.id)
        if username == request.user.username or request.user.profile.follows.filter(user__username=username):
            # Self Profile
            return render(request, 'user.html', {'user': user, 'blogPosts': posts, 'username': request.user.username, })
        return render(request, 'user.html', {'user': user, 'blogPosts': posts, 'follow': True, 'username': request.user.username,})
    users = User.objects.all().annotate(blogpost_count=Count('blogpost'))
    posts = map(get_latest, users)
    obj = zip(users, posts)
    blogpost_form = BlogPostForm(data=request.POST) if request.method == 'POST' else BlogPostForm()
    return render(request,
                  'profiles.html',
                  {'obj': obj, 'next_url': '/users/',
                   'blogpost_form': blogpost_form,
                   'username': request.user.username, })


@login_required
def follow(request):
    if request.method == "POST":
        follow_id = request.POST.get('follow', False)
        if follow_id:
            try:
                user = User.objects.get(id=follow_id)
                if request.user.profile.follows.filter(user=user).exists():
                    request.user.profile.follows.remove(user.profile)
                else:
                    request.user.profile.follows.add(user.profile)
            except ObjectDoesNotExist:
                return redirect('/users/'+user.username)
    return redirect('/users/'+user.username)
