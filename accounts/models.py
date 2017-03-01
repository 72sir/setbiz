# coding: utf8
import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Модифицируем поле email.
# _meta это экземпляр django.db.models.options.Options, который хранит данные о модели.
# Это немного хак, но я пока не нашел более простого способа переопределить поле из базовой модели.
AbstractUser._meta.get_field('email')._unique = True
AbstractUser._meta.get_field('email').blank = False


class User(AbstractUser):
    # Добавляем поля аватара. null=True не нужен т.к. в БД это обычное текстовое поле.
    # max_length=1000 - по умолчанию значение 100, пару раз натыкался на глюки при длинных названиях файлов,
    # может в 1.5 уже и не нужно, но там все так же 100.
    avatar = models.ImageField(_(u'avatar'), upload_to='static/accounts/avatar/%Y/%m/', blank=True, max_length=1000)
    # Добавляем поле дня рождения.
    birthday = models.DateField(_(u'birthday'), blank=True, null=True)
    passWallet = models.CharField(_(u'passWallet'), max_length=16, blank=True, null=True)
    phone_number = models.CharField(_(u'phone_number'), max_length=16, null=True, blank=True)
    city = models.CharField(_(u'city'), max_length=24, null=True, blank=True)
    adress = models.CharField(_(u'adress'), max_length=160, null=True, blank=True)
    parent = models.ForeignKey('User', blank=True, unique=False, null=True)
    structure = models.IntegerField(default=0)
    active_is_structure = models.IntegerField(default=0)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.datetime.now(), blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = u'User profiles'
