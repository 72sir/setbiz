# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from office import views

urlpatterns = [
    # Поиск анкеты по пользователю
    url(r'^anketa/(?P<id_user>\d+)/$', views.anketa),
    # Активация кошелька
    url(r'^wallet/$', views.wallet, name="wallet"),
    # Точно не помню что это - скорее всего удаление инфо пакета
    url(r'^wallet/delete/(?P<id_deleteKey>\w+)/$', views.deleteKey, name="deleteKey"),


    ############################payment##################################
    # Первая ссылка payment определяет метод действий, без явного определения
    url(r'^wallet/payment/$', views.payment),
    # Нашли пакет, вводим пин код и производим оплату
    url(r'^wallet/payment/send/pay/$', views.payKey),
    # Вторая ссылка payment уже требует ключ активации заказа
    url(r'^wallet/payment/(?P<id_payKey>\w+)/$', views.payment_key),
    ############################transfer##################################

    # Первая ссылка payment определяет метод действий, без явного определения
    url(r'^wallet/transfer/$', views.transfer, name="transfer"),
    # Вторая ссылка payment уже требует ключ активации заказа
    url(r'^wallet/transfer/(?P<id_payKey>\w+)/$', views.transfer, name="transfer"),
    # В третью ссылку уже отправляем найденного пользователя и данные с формы
    url(r'^wallet/transfer/(?P<id_payKey>\w+)/money/$', views.transferMoney, name="transfer"),

    url(r'^changeInfo/$', views.changeInfo, name="changeInfo"),
    url(r'^sendmail/$', views.sendmail, name="sendmail"),

    # Главная страница кабинета
    url(r'^$', views.office, name="office"),

]