# coding: utf-8
from __future__ import unicode_literals
from accounts.models import User
from django.db import models
from django.utils import timezone


# Create your models here.

# Cущности:
# сообщения которые содержат номер переписки
# Переписка которая содержит тему
# Пользователь - пользователь - переписка


# Таблица: ПОЛЬЗОВАТЕЛЬ _ ПОЛЬЗОВАТЕЛЬ _ ПЕРЕПИСКА
class massege_user(models.Model):
    user_one = models.ForeignKey(User, related_name='user_one')
    user_two = models.ForeignKey(User, related_name='user_two')
    team = models.CharField(max_length=250, default="Общение")


# Таблица: СООБЩЕНИЕ: ПЕРЕПИСКА, ТЕКСТ, ДАТА
class message_message(models.Model):
    correspondents = models.ForeignKey(massege_user, related_name='correspondents_message_message')
    user_send = models.ForeignKey(User, related_name='user_')
    massage = models.TextField(max_length=3050, default='')
    date = models.DateTimeField(auto_now_add=True)

    def publish(self):
        self.date = timezone.now()
        self.save()
