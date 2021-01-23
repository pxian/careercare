"""JobPillar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from . import views
from django.contrib import admin
from django.conf.urls import url, include
from django.views.generic.base import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^employers/homepage/', TemplateView.as_view(template_name='homepage.html')),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/', include('customadmin.urls')),
    url(r'^booking/', include('booking.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^employers/', include('employers.urls')),
    url(r'^home/', include('home.urls')),
    url(r'^insights/', include('insights.urls')),
    url(r'^jobads/', include('jobads.urls')),
    url(r'^resumeanalyzer/', include('resumeanalyzer.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^searchjob/', include('searchjob.urls')),
    url(r'^users/', include('users.urls')),
    url('', include('django.contrib.auth.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
