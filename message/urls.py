# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from message import views


urlpatterns = [
    #
    url(r'^send/(?P<id_user>\d+)/$', views.send_message, name="send_message_index"),
    url(r'^$', views.index, name="message_index"),
]
