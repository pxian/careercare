from django.contrib import admin
from .models import Employee,Freelancer
from import_export.admin import ImportExportModelAdmin

@admin.register(Employee,Freelancer)
# admin.site.register(Employee)
# admin.site.register(Freelancer)

# Register your models here.
class ViewAdmin(ImportExportModelAdmin):
    pass