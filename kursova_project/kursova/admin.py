from django.contrib import admin

# Register your models here.
from .models import UserProfile, Comment, Post, Images


class ProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'sex', 'birth_date', 'country','city','avatar')
    list_display = ('user', 'sex', 'birth_date', 'avatar')


admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Images)
