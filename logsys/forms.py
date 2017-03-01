# -*- coding: utf-8 -*-
from django import forms
from accounts.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Электронный адрес'}))
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    parent = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'parent')


class LoginForm(forms.Form):
    username = forms.CharField()

