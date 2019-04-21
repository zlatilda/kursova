# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

import datetime
from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from django.db.models.manager import Manager
from django.template.defaultfilters import slugify
from django.db.models import Count
import json
from django.utils.translation import ugettext_lazy


try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
else:
    User = settings.AUTH_USER_MODEL


class PublishedManager(Manager):
    def get_query_set(self):
        return super(PublishedManager, self).get_query_set().filter(status='Open')


@python_2_unicode_compatible
class Poll(models.Model):
    STATUS = (
        ('Open', 'Open'),
        ('Closed', 'Closed'),
     )
    title = models.CharField(max_length=250, verbose_name=_('question'))
    description = models.TextField(blank=True, null=True)
    date = models.DateField(verbose_name=_('date'), default=datetime.date.today)
    final_date = models.DateField(default=datetime.date.today)
    status = models.CharField(max_length=30, default='Open', choices=STATUS)
    thumb = models.ImageField(default='default.png', blank=True)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-date']
        verbose_name = _('poll')
        verbose_name_plural = _('polls')

    def __str__(self):
        return self.title

    def get_vote_count(self):
        return Vote.objects.filter(poll=self).count()

    vote_count = property(fget=get_vote_count)

    def get_cookie_name(self):
         return 'poll_%s' % self.pk

    def get_comment_count(self):
        from kursova.models import Comment
        return Comment.objects.filter(poll=self).count()

    def check_active_status(self):
        if datetime.date.today() > self.final_date:
            self.status = "Closed"
        else:
            self.status = "Open"
        self.save()


    def sexes(self):
        sexes = []
        from kursova.models import UserProfile
        count = 0
        voted = Vote.objects.filter(poll=self)
        for x in voted:
            if UserProfile.objects.filter(user=x.user, sex='Male'):
                count += 1
        sexes.append(count)
        count = 0
        for x in voted:
            if UserProfile.objects.filter(user=x.user, sex='Female'):
                count += 1
        sexes.append(count)
        count = 0
        for x in voted:
            if UserProfile.objects.filter(user=x.user, sex='Battle helicopter'):
                count += 1
        sexes.append(count)
        return sexes

    """def countries(self):
        from kursova.models import UserProfile
        val = UserProfile.objects.values('country').annotate(dcount=Count('country'))
        users = val.all().values_list('user', flat=True)
        cntrs = val.all().values_list('country', flat=True)
        cntrs = list(cntrs)
        cntrs_for_js = json.dumps(cntrs)
        ppl = val.all().values_list('dcount', flat=True)
        ppl = list(ppl)
        context = {
            'cntrs_for_js': cntrs_for_js,
            'ppl': ppl,
        }
        return context"""

    def countries(self):
        from kursova.models import UserProfile
        count = 0
        voted = Vote.objects.filter(poll=self)
        val = UserProfile.objects.values('country')
        cntrs = val.all().values_list('country', flat=True)
        cntrs = list(cntrs)
        dict = {}
        for x in voted:
            for y in cntrs:
                if UserProfile.objects.filter(user=x.user, country=y):
                    if y in dict:
                        count = dict[y] + 1
                    else:
                        count += 1
                    dict[y] = count
                    break
            count = 0
        countries_keys = list(dict.keys())
        countries_values = list(dict.values())
        countries_keys = json.dumps(countries_keys)
        context = {
            'dict': dict,
            'countries_keys': countries_keys,
            'countries_values': countries_values,
        }
        return context

    def age(self):
        from kursova.models import UserProfile
        voted = Vote.objects.filter(poll=self)

        dict = {}
        count  = 0

        for x in voted:
            if UserProfile.objects.filter(user=x.user):
                obj = UserProfile.objects.get(user=x.user)
                if (datetime.date.today() - obj.birth_date).days /365.25 <= 18:
                    if "under 18" in dict:
                        count = dict["under 18"] + 1
                    else:
                        count += 1
                    dict["under 18"] = count
                elif 18 < (datetime.date.today() - obj.birth_date).days /365.25 <= 40:
                    if "18+" in dict:
                        count = dict["18+"] + 1
                    else:
                        count += 1
                    dict["18+"] = count
                elif 40 < (datetime.date.today() - obj.birth_date).days /365.25 <= 60:
                    if "40+" in dict:
                        count = dict["40+"] + 1
                    else:
                        count += 1
                    dict["40+"] = count
                elif 60 < (datetime.date.today() - obj.birth_date).days /365.25:
                    if "60+" in dict:
                        count = dict["60+"] + 1
                    else:
                        count += 1
                    dict["60+"] = count
                count = 0
        age_keys = list(dict.keys())
        age_values = list(dict.values())
        age_keys = json.dumps(age_keys)
        context = {
            'age_keys': age_keys,
            'age_values': age_values,
        }
        return context

    def average_age(self):
        from kursova.models import UserProfile
        voted = Vote.objects.filter(poll=self)

        sum = 0
        count = 0

        for x in voted:
            if UserProfile.objects.filter(user=x.user):
                obj = UserProfile.objects.get(user=x.user)
                sum += (datetime.date.today() - obj.birth_date).days / 365.25
                count += 1

        return round(sum/count, 2)

@python_2_unicode_compatible
class Item(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    value = models.CharField(max_length=250, verbose_name=_('value'))
    pos = models.SmallIntegerField(default='0', verbose_name=_('position'))

    class Meta:
        verbose_name = _('answer')
        verbose_name_plural = _('answers')
        ordering = ['pos']

    def __str__(self):
        return u'%s' % (self.value,)

    def get_vote_count(self):
        return Vote.objects.filter(item=self).count()
    vote_count = property(fget=get_vote_count)


@python_2_unicode_compatible
class Vote(models.Model):
    from kursova.models import UserProfile
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, verbose_name=_('poll'))
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name=_('voted item'))
    ip = models.GenericIPAddressField(verbose_name=_('user\'s IP'))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                             verbose_name=_('user'))
    datetime = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = _('vote')
        verbose_name_plural = _('votes')

    def __str__(self):
        if isinstance(User, str):
            UserModel = get_user_model()
        else:
            UserModel = User

        if isinstance(self.user, type(UserModel)):
            username_field = getattr(User, 'USERNAME_FIELD', 'username')
            return getattr(User, username_field, '')
        return self.ip
