
from django.conf.urls import url
from logsys import views


urlpatterns = [
    url(r'^contacts/$', views.contacts),
    url(r'^contract/$', views.oferta),
    url(r'^news/$', views.news),
    url(r'^auth/register/$', views.RegisterView),
    url(r'^auth/register/findUsers/$', views.findUsers),
    url(r'^auth/login/$', views.LoginFormView),
    url(r'^auth/logout/$', views.LogoutView),
    url(r'^auth/new/$', views.new),
    url(r'^(?P<id_parent>\d+)/$', views.index, name="index"),
    url(r'^auth/(?P<activation_key>\w+)/$', views.register_confirm, name="register_confirm"),
    url(r'^$', views.index, name="index"),
]
