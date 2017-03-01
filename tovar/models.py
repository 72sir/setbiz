# coding: utf8
from __future__ import unicode_literals
import datetime
from django.utils import timezone
from django.db import models
from django.utils.translation import ugettext_lazy as _
from accounts.models import User


# Create your models here.


################################################################################
# Таблица по свойствам товара
# компания
# тип
# марка
################################################################################
class Attribute(models.Model):
    name = models.CharField(max_length=255)
    # Здесь выбираем к какой категории относится наименование
    # пункт назначения, назначение, место назначения, предназначение
    destination = models.BooleanField(default=False)
    # Наименование компании
    company = models.BooleanField(default=False)
    # Тип оборудования
    type = models.BooleanField(default=False)
    # Марка модель оборудования
    model = models.BooleanField(default=False)
    # Создаем родителя для company type model
    # что облегчит поиск товара
    parent = models.ForeignKey('Attribute', default=None, related_name="parent_attribure", null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.name


################################################################################
# ФОТО - ТОВАР
################################################################################
class FotoTovar(models.Model):
    avatar = models.ImageField(_(u'avatar'), upload_to='static/product/avatar/%Y/%m/', blank=True, max_length=1000)
    product = models.ForeignKey('Product', related_name="FotoTovar_product")


# Создаем класс продукта
class Product(models.Model):
    # Добавляем поля аватара. null=True не нужен т.к. в БД это обычное текстовое поле.
    # Для этого поля требуется библиотека Pillow
    # max_length=1000 - по умолчанию значение 100, пару раз натыкался на глюки при длинных названиях файлов,
    # может в 1.5 уже и не нужно, но там все так же 100.
    # что бы _(u'avatar') не выдавало ошибку добавляем "from django.utils.translation import ugettext_lazy as _"
    avatar = models.ImageField(_(u'avatar'), upload_to='static/product/avatar/%Y/%m/', blank=True, max_length=1000)
    # Наименование
    name = models.CharField(max_length=150)
    # Краткое описание
    title = models.CharField(max_length=400)
    # Подробное описание
    text = models.TextField()
    # Цена продукта
    # тз такое если цена 0, значить ценника на него нет
    # при необходимости можно оставлять blank = True, null = True
    price = models.PositiveIntegerField(default=0)
    # Дата добавления продукта
    created_date = models.DateTimeField(default=timezone.now)
    # Дата продажи
    published_date = models.DateTimeField(blank=True, null=True)

    ####################################################################
    # добавим 3 свойства для товара
    destination = models.ForeignKey(Attribute, default=None, related_name="destination_producrt", null=True, blank=True)
    company = models.ForeignKey(Attribute, default=None, related_name="company_product", null=True, blank=True)
    type = models.ForeignKey(Attribute, default=None, related_name="type_product", null=True, blank=True)
    model = models.ForeignKey(Attribute, default=None, related_name="model_product", null=True, blank=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def unicode(self):
        return self.name, self.title, self.text


#######################################################
# СОЗДАЕМ ТАБЛИЦУ ЗАКАЗОВ ПОЛЬЗОВАТЕЛЬ - ПРОДУКТ
# Требуются поля:
# ПОЛЬЗОВАТЕЛЬ - ПРОДУКТ
# Ключ активации продукции - уникальный
# Статус продукции по оплате \ отправки и всем возможным видам действий
# дата оформления заказа
class OrderProduct(models.Model):
    user = models.ForeignKey(User, related_name="order_user")
    product = models.ForeignKey('Product', related_name="order_product")
    # Дата добавления продукта
    created_date = models.DateTimeField(default=timezone.now)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.datetime.now(), blank=True, null=True)
    status = models.CharField(max_length=255)
    payment = models.BooleanField(default=False)

    def unicode(self):
        return self.status


#######################################################
# СОЗДАЕМ ТАБЛИЦУ ПО РЕАЛИЗАЦИИ ТОВАРА ДЛЯ ПОЛЬЗОВАТЕЛЕЙ
# 1 пользователь который проплатил заказ
# 2 Заказ на проплату
# 3 Дата проплаты
class OrderPaymentProduct(models.Model):
    userPayment = models.ForeignKey(User, related_name="orderPaymentProduct_userPayment")
    product = models.ForeignKey('OrderProduct', related_name="orderPaymentProduct_product")
    # Дата добавления продукта
    created_date = models.DateTimeField(default=timezone.now)

    def unicode(self):
        return self.product


##############################################
# Таблица регистрации продукта при регистрации в матрице
class MatrixProduct(models.Model):
    user = models.ForeignKey(User, related_name="Matrix_product_user")
    product = models.ForeignKey('Product', related_name="MatrixProduct_product")










