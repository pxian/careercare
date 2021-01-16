from django.conf.urls import url
from . import views

app_name = 'customadmin'

urlpatterns = [
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
]
