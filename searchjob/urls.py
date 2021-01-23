from django.conf.urls import url
from . import views

app_name = 'searchjob'

urlpatterns = [
    url(r'^$', views.search, name='search'),
    url(r'^freesearch/$', views.fsearch, name='fsearch'),
    url(r'^job_app/$', views.job_app, name ='job_app'),
    url(r'^free_app/$', views.free_app, name ='free_app'),
    url(r'^(?P<id>\d+)/apply_job/$', views.apply_job, name ='apply_job'),
    url(r'^(?P<id>\d+)/apply_free/$', views.apply_free, name ='apply_free'),
    url(r'^(?P<id>\d+)/view_job/$', views.view_job, name ='view_job'),
    url(r'^(?P<id>\d+)/freeview_job/$', views.freeview_job, name ='freeview_job'),
    url(r'^service_req/$', views.service_req, name ='service_req'),
]
