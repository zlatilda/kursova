from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Comment
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
YEARS= [x for x in range(1940,2021)]

class ProfileForm(forms.ModelForm):

    #def __init__(self, *args, **kwargs):
      #  super(ProfileForm, self).__init__(*args, **kwargs)

    birth_date = forms.DateField(initial="1990-06-21" , widget=forms.SelectDateWidget(years=YEARS, attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ('birth_date', 'sex', 'country', 'city', 'avatar')
        widgets = {
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }


class RegForm(forms.ModelForm):

    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                              'id': 'name'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                             'id': 'surname'}))
    username = forms.CharField(max_length=30, help_text="Enter your username (30 letter or less)."
                               , widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'id': 'username'}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'}))
    password1 = forms.CharField(max_length=32, label='Password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password'}), )
    password2 = forms.CharField(max_length=32, label='Password confirmation',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'assert_password'}), )

    class Meta:
        model = User

        fields = ('first_name', 'last_name', 'username', 'email', 'password1',
                  'password2',)

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password1'])
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return user


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'style': 'resize:none; height: 5em;'})
        }


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = {
            'email',
            'first_name',
            'last_name',
            'password',
        }


class FillProfileForm(ProfileForm):
    class Meta:
        model = UserProfile
        fields = {
            'sex',
            'birth_date',
            'country',
            'city',
        }
