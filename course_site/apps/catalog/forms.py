from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm

from course_site.apps.catalog.models import Course


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='email:', widget=forms.TextInput(
        attrs={'class': 'form-control', 'autofocus': True, 'autocomplete': 'off', 'placeholder': "Email"}))
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(
        attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': "Username"}))
    password1 = forms.CharField(label='Пароль:', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': "Password"}))
    password2 = forms.CharField(label='Подтверждение пароля:', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': "Confirm password"}))

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')


class LoginAuthForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(
        attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': "Username", 'required': True}))
    password = forms.CharField(label='Пароль:', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': "Password", 'required': True}))

    class Meta:
        model = User
        fields = ('username', 'password')


class RequestCourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'summary', 'added_by']
