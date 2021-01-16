from django.conf.urls import url
from . import views

app_name = 'booking'

urlpatterns = [
    url(r'^$', views.booking, name='booking'),
    url(r'^(?P<id>\d+)$', views.service, name='service'),
    url(r'^(?P<id>\d+)/form$', views.bookservice, name='bookservice'),
    url(r'^markcomplete/(?P<id>\d+)/$', views.markcomplete, name='markcomplete'),
    url(r'^deletebooking/(?P<id>\d+)/$',
        views.deletebooking, name='deletebooking'),
    url(r'^complete/(?P<id>\d+)$', views.complete, name='complete'),
    url(r'^upcoming/(?P<id>\d+)$', views.upcoming, name='upcoming'),
    url(r'^cancelbooking/(?P<id>\d+)$', views.cancelbooking, name='cancelbooking'),
]
