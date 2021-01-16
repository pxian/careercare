from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'resumeanalyzer'


urlpatterns = [
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('uploadresume/', views.uploadresume, name='uploadresume'),
    path('resumelist/', views.resumelist, name='resumelist'),
    path('uploadjob/', views.uploadjob, name='uploadjob'),
    path('matchall/<int:jobid>/', views.matchall, name='matchall'),
    path('matchshortlisted/<int:jobid>/', views.matchshortlisted, name='matchshortlisted'),
    path('filter/<int:jobid>/', views.filter, name='filter'),
    path('visualise/<int:jobid>/', views.visualise, name='visualise'),
    path('visualiseshortlisted/<int:jobid>/', views.visualiseshortlisted, name='visualiseshortlisted'),
    path('visualisefilter/<int:jobid>/', views.visualisefilter, name='visualisefilter'),
    path('details/<int:resumeid>/', views.details, name='details'),
    path('history/', views.history, name='history'),
    path('result/<int:jobid>/', views.result, name='result'),
    path('shortlist/<int:resumeid>/', views.shortlist, name='shortlist'),
    path('delist/<int:resumeid>/', views.delist, name='delist'),
    path('deleteResume/<int:resumeid>/', views.deleteResume, name='deleteResume'),
    path('deleteJob/<int:jobid>/', views.deleteJob, name='deleteJob'),
    path('addNotes/<int:resumeid>/', views.addNotes, name='addNotes'),

]