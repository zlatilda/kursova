from django.db import models
from django_countries.fields import CountryField
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from poll.models import Poll


class UserProfile(models.Model):

    SEX_CHOISES = (
        ('Battle helicopter', 'Battle helicopter'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    birth_date = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=20, default='Male', choices=SEX_CHOISES)
    country = CountryField(blank_label='(Choose country)', )
    city = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set added_by during the first save.
            obj.added_by = request.user
        super().save_model(request, obj, form, change)


class Comment(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length = 500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.poll.title, str(self.user.username))

