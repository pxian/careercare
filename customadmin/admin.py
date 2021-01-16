from django.contrib import admin
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required

admin.site.site_header = 'Administrator'
admin.site.site_url = '/admin/dashboard'
# admin.site.login = staff_member_required(
#     admin.site.view_on_site, login_url=settings.LOGIN_REDIRECT_URL)
