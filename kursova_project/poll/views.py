# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import redirect

from .utils import set_cookie
from .models import Poll, Item, Vote
from kursova.models import *
from kursova.forms import *
from django.views.generic import RedirectView
from django.shortcuts import get_object_or_404
from django.urls import reverse


def vote(request, poll_pk):
    if request.is_ajax():
        try:
            poll = Poll.objects.get(pk=poll_pk)
        except:
            return HttpResponse('Wrong parameters', status=400)

        item_pk = request.GET.get("item", False)
        if not item_pk:
            return HttpResponse('Wrong parameters', status=400)

        try:
            item = Item.objects.get(pk=item_pk)
        except:
            return HttpResponse('Wrong parameters', status=400)

        if request.user.is_authenticated:
            user = request.user
        else:
            user = None

        Vote.objects.create(
            poll=poll,
            ip=request.META['REMOTE_ADDR'],
            user=user,
            item=item,
        )

        response = HttpResponse(status=200)
        set_cookie(response, poll.get_cookie_name(), poll_pk)

        return response
    return HttpResponse(status=400)


def poll(request, poll_pk):
    try:
        poll = Poll.objects.get(pk=poll_pk)
    except Poll.DoesNotExists:
        return HttpResponse('Wrong parameters', status=400)

    items = Item.objects.filter(poll=poll)
    comments = Comment.objects.filter(poll=poll).order_by('-timestamp')
    if poll.status == 'Closed':
        template = "result.html"
    else:
        if request.user.is_authenticated:
            voted = Vote.objects.filter(poll=poll, user=request.user)
            if voted:
                template = 'result.html'
            else:
                template = 'poll.html'
        elif request.user.is_anonymous:
            template = 'result.html'

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            comment = Comment.objects.create(poll=poll, user=request.user, content=content)
            comment.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        comment_form = CommentForm()

    return render(request, template, {
        'poll': poll,
        'items': items,
        'comments': comments,
        'comment_form': comment_form,
    })


def result(request, poll_pk):
    try:
        poll = Poll.objects.get(pk=poll_pk)
    except Poll.DoesNotExists:
        return HttpResponse('Wrong parameters', status=400)

    items = Item.objects.filter(poll=poll).order_by('-id')
    comments = Comment.objects.filter(poll = poll)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            comment = Comment.objects.create(poll=poll, user=request.user, content=content)
            comment.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        comment_form = CommentForm()

    return render(request, "result.html", {
        'poll': poll,
        'items': items,
        'comments': comments,
        'comment_form': comment_form,
    })
