from django.conf.urls import url
from . import views

app_name = 'employers'

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^welcome/$', views.welcome, name='welcome'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^password/$', views.password, name='password'),
    url(r'^company/$', views.company, name='company'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^deleteaccount/$', views.deleteaccount, name='deleteaccount'),
]
