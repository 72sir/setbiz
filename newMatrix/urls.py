# coding: utf-8
from django.conf.urls import url
from newMatrix import views


urlpatterns = [
    # Регистрация пользователя в столе по id рекомендателя
    url(r'^(?P<id_desk>\d+)/$', views.newMatrix_SearchUserInLargeDesk),
    url(r'^$', views.newMatrix_index),
]
