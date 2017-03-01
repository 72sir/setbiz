# coding: utf-8
from __future__ import unicode_literals
from accounts.models import User
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.


########################################
# Учет входа и выплат по столам
# выплата идет по закрытию малого стола
# товар при входе в матрицу
########################################
from tovar.models import Product


class MatrixMoneyPay(models.Model):
    inMatrix = models.PositiveIntegerField(default=1000)
    outMatrix = models.PositiveIntegerField(default=1500)
    tovarMatrix = models.ForeignKey(Product, related_name="MatrixMoneyPay_tovarMatrix", default=30)


###################################### ###################################### ######################################
# Малый стол заказов
# он состоит из 3 пользователей для определения сколько еще свободных мест нужно заполнить
# что бы создать из них большой стол заказов
###################################### ###################################### ######################################
class newMatrix_smallDesk(models.Model):
    smallDesk_UserInHead = models.ForeignKey(User, default=19, related_name="smallDesk_1", null=False)
    smallDesk_RightPlace = models.ForeignKey(User, default=None, related_name="smallDesk_2", blank=True, null=True)
    smallDesk_LeftPlace = models.ForeignKey(User, default=None, related_name="smallDesk_3", blank=True, null=True)
    smallDesk_matrixMoneyPay = models.ForeignKey(MatrixMoneyPay, related_name="smallDesk_matrixMoneyPay", default=1)


###################################### ###################################### ######################################
# Большой стол зказов
# он состоит из 1 человека который стоит в голове на выплату и 2 малых столов, которые нужно закрыть и сделать
# их большими столами
###################################### ###################################### ######################################
class newMatix_largeDesk(models.Model):
    largeDesk_User = models.ForeignKey(User, null=False, blank=False, related_name="largeDesk_User")
    largeDesk_RightDesk = models.ForeignKey(newMatrix_smallDesk, null=True, blank=True, related_name="largeDeskOneDesk")
    largeDesk_LeftDesk = models.ForeignKey(newMatrix_smallDesk, null=True, blank=True, related_name="largeDeskTwoDesk")


###################################### ###################################### ######################################
# Учет мест в малых столах
# В каждом малом столе нужно вести учет мест, что бы знать время когда его закрыть и открыть 1 большой стол
###################################### ###################################### ######################################
class newMatrix_freePlaceSmallDesk(models.Model):
    freeSpaceSmallDesk_smallDesk = models.ForeignKey(newMatrix_smallDesk, null=False, blank=False)
    freeSpaceSmallDesk_freePlace = models.IntegerField(null=False, blank=False, default=2)


###################################### ###################################### ######################################
# ПОЛЬЗОВАТЕЛЬ - Маленький СТОЛ
###################################### ###################################### ######################################
class newMatrix_UserDesk(models.Model):
    UserDesk_User = models.ForeignKey(User, related_name="UserDesk_User", null=False, blank=False)
    UserDesk_Desk = models.ForeignKey(newMatrix_smallDesk, related_name="UserDesk_Desk", null=False, blank=False)


###################################### ###################################### ######################################
# ПОЛЬЗОВАТЕЛЬ - Большой СТОЛ
###################################### ###################################### ######################################
class newMatrix_UserLargeDesk(models.Model):
    UserLargeDesk_User = models.ForeignKey(User, related_name="UserLargeDesk_User", null=False, blank=False)
    UserLargeDesk_Desk = models.ForeignKey(newMatix_largeDesk, related_name="UserLargeDesk_Desk", null=False, blank=False)


###################################### ###################################### ######################################
# БОЛЬШОЙ СТОЛ - МАЛЕНЬКИЙ СТОЛ
###################################### ###################################### ######################################
class newMatrix_LargeDeskSmallDesk(models.Model):
    LargeDeskSmallDesk_SmallDesk = models.ForeignKey(newMatrix_smallDesk, related_name="SmallDesk_Desk_", null=False, blank=False)
    LargeDeskSmallDesk_LargeDesk = models.ForeignKey(newMatix_largeDesk, related_name="LargeDesk_Desk_", null=False, blank=False)





