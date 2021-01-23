from django.conf.urls import url
from . import views

app_name = 'users'

urlpatterns = [
    url(r'^register', views.register, name='register'),
    url(r'^logout/$', views.log_out, name='logout'),
    url(r'^login/$', views.log_in, name='login'),
    url(r'^create_profile/$', views.create_profile, name ='create_profile'),
    url(r'^edit_profile/$', views.edit_profile, name ='edit_profile'),
    url(r'^edit_fprofile/$', views.edit_profile, name ='edit_fprofile'),
    # url(r'^view_jobs/$', views.view_jobs, name ='view_jobs'),
]