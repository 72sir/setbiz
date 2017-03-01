# coding: utf8
from __future__ import unicode_literals
from django.db import models
from accounts.models import User
from django.utils import timezone

# Create your models here.


###################################################################################
# Создаем таблицу с пользовательскими кошельками
###################################################################################
class UserWallet(models.Model):
    # Пользователь
    UserWallet_user = models.ForeignKey(User, default=1)
    # Денежки на кошельке
    UserWallet_walletPrice = models.IntegerField(default=0)
    # Бонусы на кошельке
    UserWallet_walletBonuce = models.IntegerField(default=0)
    ### Пароль кошелька или пин
    UserWallet_password = models.CharField(blank=False, max_length=50)
    # Дата созданеия кошелька
    UserWallet_dateCreate = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    # Активность кошелька - под вопросом
    UserWallet_IsActive = models.BooleanField(default=False)

    def publish(self):
        self.ModelWallet_dateCreate = timezone.now()
        self.save()
