from .models import UserProfile, Comment
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
from django.views.generic import TemplateView


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

    template = "list.html"
    hot = Poll.objects.filter(status='Open')
    sort_hot = sorted(hot, key=lambda t: t.get_vote_count())
    sort_hot.reverse()
    query = request.GET.get('q')
    if query:
        items = Poll.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:
        items = Poll.objects.all()
    content = {
        'items': items,
        'hot': sort_hot[:5],
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

