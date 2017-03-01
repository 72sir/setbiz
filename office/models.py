# -*- coding: utf-8 -*-
from django.db import models
from accounts.models import User

# Create your models here.


###############################################################################
# История перевода денежных средств по аккаунтам
###############################################################################
class Office_HistoryTransfer(models.Model):
    # Кто перевел
    HistoryTransfer_userTransfer = models.ForeignKey(User, blank=False, null=False)
    # Кому перевел (сохраняю как интежер так как не 2 ключа выдают ошибку)
    HistoryTransfer_userGets = models.IntegerField(blank=False, null=False)
    # Сумма перевода
    HistoryTransfer_TransferAmount = models.IntegerField(default=0, blank=False, null=False)





