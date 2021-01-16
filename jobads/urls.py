from django.conf.urls import url
from . import views

app_name = 'jobads'

urlpatterns = [
    url(r'^$', views.jobads, name='jobads'),
    url(r'^createjob/$', views.createjob, name='createjob'),
    url(r'^editjob/(?P<id>\d+)/$', views.editjob, name='editjob'),
   url(r'^view_ranking/(?P<id>\d+)/(?P<jobid>\d+)/$', views.view_ranking, name='view_ranking'),
    url(r'^deletejob/(?P<id>\d+)/$', views.deletejob, name='deletejob'),
    url(r'^(?P<id>\d+)/$', views.unprocessed, name='unprocessed'),
    url(r'^(?P<job>\d+)/(?P<cand>\d+)/candidate$',
        views.candidate, name='candidate'),
    url(r'^(?P<id>\d+)/shortlist$', views.shortlist, name='shortlist'),
    url(r'^(?P<id>\d+)/interview$', views.interview, name='interview'),
    url(r'^(?P<id>\d+)/notsuitable$', views.notsuitable, name='notsuitable'),
    url(r'^(?P<job>\d+)/(?P<cand>\d+)/invitation$',
        views.invitation, name='invitation'),
    url(r'^(?P<id>\d+)/invited$', views.invited, name='invited'),
]
