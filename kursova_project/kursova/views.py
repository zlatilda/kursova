from django.urls import reverse

from .models import UserProfile, Comment, Post
from .forms import *
from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from kursova.forms import RegForm, ProfileForm
from poll.models import *
from django.contrib.auth.models import User
from django.core import serializers
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.generic import TemplateView, RedirectView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_detail(request, slug):

    template = 'poll.html'
    items = get_object_or_404(Poll, slug=slug)
    context = {
        'items': items,
    }
    return render(request, template, context)


def index(request):
    template = 'list.html'
    items = Poll.objects.all().order_by('-date')
    hot = Poll.objects.filter(status='Open')
    sort_hot = sorted(hot, key = lambda t: t.get_vote_count())
    sort_hot.reverse()

    page = request.GET.get('page', 1)

    paginator = Paginator(items, 10)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context = {

        'items': items,
        'hot':sort_hot[:5],
    }
    return render(request, template, context)


def active(request):
    template = 'list.html'
    items = Poll.objects.filter(status='Open').order_by('-date')
    hot = Poll.objects.filter(status='Open')
    sort_hot = sorted(hot, key=lambda t: t.get_vote_count())
    sort_hot.reverse()
    context = {

        'items': items,
        'hot': sort_hot[:5],
    }
    return render(request, template, context)

def closed(request):
    template = 'list.html'
    items = Poll.objects.filter(status='Closed').order_by('-date')
    hot = Poll.objects.filter(status='Open')
    sort_hot = sorted(hot, key=lambda t: t.get_vote_count())
    sort_hot.reverse()
    context = {

        'items': items,
        'hot': sort_hot[:5],
    }
    return render(request, template, context)

def search(request):

    template = "search.html"
    hot = Poll.objects.filter(status='Open')
    sort_hot = sorted(hot, key=lambda t: t.get_vote_count())
    sort_hot.reverse()
    query = request.GET.get('q')
    if query:
        items = Poll.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        articles = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
    else:
        items = Poll.objects.all()
        articles = Post.objects.all()
    content = {
        'items': items,
        'hot': sort_hot[:5],
        'articles': articles,
    }

    return render(request, template, content)


def signup(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('kursova:create_profile')
    else:
        form = RegForm()
    return render(request, 'register.html', {'form': form})


def create_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile_form.user = request.user
            #profile_form.save()

            return redirect('kursova:index')
    else:
        profile_form = ProfileForm()
        return render(request, 'register.html', {'profile': profile_form})


def get_user_profile(request, username):
    template = 'user_page.html'
    user = User.objects.get(username=username)
    comments = Comment.objects.filter(user = user).order_by('-timestamp')
   # votes = Vote.objects.filter(user=user)
    profile = UserProfile.objects.get(user=user)
    context = {
        'user': user,
        'comments': comments,
      #  'votes': votes,
        'profile': profile,
    }
    return render(request, template, context)


def user_settings(request):

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('kursova:index')
        else:
            return redirect('user-settings')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form, }
        return render(request, 'settings.html', args)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user = request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('kursova:index')
        else:
            return redirect('change-password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'change_password.html', args)


def create_profile(request):
    #template = 'profile.html'
    post = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, instance=post)
        if profile_form.is_valid():
            profile_form = profile_form.save(commit=False)
            profile_form.user = request.user
            profile_form.save()
            return redirect('kursova:get_user_profile', request.user.username)
    else:
        profile_form = ProfileForm(instance=post)
    return render(request, 'profile.html', {'profile_form': profile_form})


def post_list(request):

    template = 'post.html'
    items = Post.objects.order_by('-created')
    context = {

       'items': items,
    }

    return render(request, template, context)


def article_detail(request, post_pk):

    template = 'post_detail.html'
    post = get_object_or_404(Post, pk=post_pk)
    rand_poll = Poll.objects.filter(status='Open').order_by('?')
    rand_post = Post.objects.order_by('?')

    images = Images.objects.filter(slug=post.slug)

    context = {
        'post': post,
        'rand_poll': rand_poll[:5],
        'rand_post': rand_post[:5],
        'images': images,
    }
    return render(request, template, context)


class PostLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        print(slug)
        obj = get_object_or_404(Post, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_


def comment_delete(request, pk):
    comment = Comment.objects.get(pk=pk)
    if comment.user == request.user:
        comment.is_removed = True
        comment.save()
        comment.delete()

    return redirect(request.META['HTTP_REFERER'])




