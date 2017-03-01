# coding: utf-8
"""my_product URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
# Подключаем наш модуль продукта
from tovar import views

urlpatterns = [
    # Создаем ссылку для поиска товара по запросу
    url(r'^search/$', views.searchProducrt),
    # Создаем заказ на продукт по пользователю
 url(
r'^destination/(?P<id_destination>\d+)/company/(?P<id_company>\d+)/type/(?P<id_type>\d+)/model/(?P<id_model>\d+)/orders/$',
        views.orders_product),
    # url ссылка на наш продукт
    url(r'^destination/(?P<id_destination>\d+)/$', views.view_destination),
    url(r'^destination/(?P<id_destination>\d+)/company/(?P<id_company>\d+)/$', views.view_company),
    url(r'^destination/(?P<id_destination>\d+)/company/(?P<id_company>\d+)/type/(?P<id_type>\d+)/$', views.view_type),
    url(
r'^destination/(?P<id_destination>\d+)/company/(?P<id_company>\d+)/type/(?P<id_type>\d+)/model/(?P<id_model>\d+)/$',
        views.view_model),
    url(r'^$', views.product),
]
