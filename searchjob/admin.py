from django.contrib import admin
from .models import JobAd, AppliedJob, ServiceRequest,ViewedJob, Freelance
from import_export.admin import ImportExportModelAdmin
# Register your models here.

@admin.register(JobAd)
@admin.register(AppliedJob)
@admin.register(ServiceRequest)
@admin.register(ViewedJob)
@admin.register(Freelance)


class ViewAdmin(ImportExportModelAdmin):
    pass