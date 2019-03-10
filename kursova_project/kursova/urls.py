from django.conf.urls import url, include
from .views import *
from django.contrib.auth import views as auth
app_name = 'kursova'

urlpatterns = [
    url(r'^home/$', index, name='index'),
    url(r'registration/', signup, name='signup'),
    url(r'post/(?P<slug>[-\w]+)/', post_detail, name='post'),
    url(r'result/', search, name="search"),
    url(r'user/(?P<username>[-\w]+)/', get_user_profile, name="usr_pg"),
]
