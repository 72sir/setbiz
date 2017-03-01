# coding: utf8
from .models import User
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


# Допиливаем форму добавления пользователя. В Meta.model указываем нашу модель.
# Поля указывать нет необходимости т.к. они переопределяются в UserAdmin.add_fieldsets
class AdminUserAddForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'username',
                  'email',
                  'parent',
                  )

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


# Допиливаем форму редактирования пользователя. В Meta.model указываем нашу модель.
class AdminUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        exclude = ('user',)



# Допиливаем форму редактирования пользователя. В Meta.model указываем нашу модель.
class UserChangeForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(max_length=16)
    city = forms.CharField(max_length=24)
    adress = forms.CharField(max_length=160)

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'username',
                  'email',
                  'phone_number',
                  'city',
                  'adress',
                  'birthday')

        exclude = ('password')


