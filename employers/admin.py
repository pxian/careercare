from django.contrib import admin
from .models import Employer, Individual


admin.site.register([Employer, Individual])
