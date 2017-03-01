# coding: utf-8

from django.conf.urls import url, include
from django.contrib import admin
from logsys import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # Ошибка
    url(r'^errors404/', views.errors404, name="errors404"),
    # в оффисе находятся ссылки на анкеты пользователей
    url(r'^office/', include('office.urls')),
    # Стол заказов
    url(r'^orders/', include('newMatrix.urls'), name="newMarketing"),
    # Распологаются сообщения пользователей
    url(r'^message/', include('message.urls')),
    # По данной ссылке располагаем всю продукцию для продажи
    url(r'^tovar/', include('tovar.urls')),
    # Главная страница сайта index
    url(r'^', include('logsys.urls')),
]