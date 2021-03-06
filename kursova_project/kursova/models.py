from django.db import models
from django_countries.fields import CountryField
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from poll.models import Poll
from django.db.models.signals import post_save
from django.urls import reverse
from django.conf import settings

class UserProfile(models.Model):

    SEX_CHOISES = (
        ('Battle helicopter', 'Battle helicopter'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    birth_date = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=20, default='Male', choices=SEX_CHOISES)
    country = CountryField(blank_label='(Choose country)',)
    city = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    def create_profile(sender, **kwargs):
        if kwargs['created']:
            user_profile = UserProfile.objects.create(user=kwargs['instance'])

    post_save.connect(create_profile, sender=User)


class Post(models.Model):

    STATUS_CHOISES = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
    )

    title = models.CharField(max_length=30)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_likes')
    slug = models.SlugField(max_length=250, unique=True)
    status = models.CharField(max_length=10, default='Draft', choices=STATUS_CHOISES)
    thumb = models.ImageField(default='default.png', blank=True)
    poll_link = models.TextField(default='none')

    def get_absolute_url(self):
        return reverse("kursova:article_detail", kwargs={"post_pk": self.pk})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_like_url(self):
        return reverse("kursova:like-toggle", kwargs={"slug": self.slug})

    def get_api_like_url(self):
        return reverse("blog:like-api-toggle", kwargs={"slug": self.slug})


def get_image_filename(instance, filename):
    title = instance.post.title
    slug = slugify(title)
    return "post_images/%s-%s" % (slug, filename)


class Images(models.Model):
    #post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    slug = models.TextField(default='none')
    image = models.ImageField(default='default.png', blank=True)

    def __str__(self):
        return self.image.name


class Comment(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length = 500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.poll.title, str(self.user.username))

    def get_absolute_url(self):
        return reverse("poll:poll", kwargs={"poll_pk": self.pk})


