from django.conf.urls import url, include
from .views import *
from django.contrib.auth import views as auth
from . import views as core_view
app_name = 'kursova'

urlpatterns = [
    url(r'^home/$', index, name='index'),
    url(r'registration/', signup, name='signup'),
    url(r'post/(?P<slug>[-\w]+)/', post_detail, name='post'),
    url(r'result/', search, name="search"),
    url(r'user/(?P<username>[-\w]+)/', get_user_profile, name="usr_pg"),
    url(r'create-profile/', create_profile, name='create_profile'),
    url(r'active/', active, name="active"),
    url(r'closed/', closed, name="closed"),
    url(r'profile/(?P<username>[-\w]+)/', get_user_profile, name='get_user_profile'),
    url(r'user-settings/', user_settings, name='user_settings'),
    url(r'change-password/', change_password, name='change_password'),
    url(r'delete-comment/', DeleteComment.as_view(), name='DeleteComment'),
    url(r'articles/', post_list, name='post_list'),
    url(r'artcl/(?P<post_pk>[-\w]+)/', article_detail, name="article_detail"),
    url(r'(?P<slug>[-\w]+)/like/', core_view.PostLikeToggle.as_view(), name="like-toggle"),
]
