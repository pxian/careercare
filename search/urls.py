from django.conf.urls import url
from . import views

app_name = 'search'

urlpatterns = [
    url(r'^$', views.search, name='search'),
    url(r'^(?P<id>\d+)/candidate$', views.candidate, name='candidate'),
    url(r'^send/message/(?P<id>\d+)/$', views.contact, name='contact'),
]
