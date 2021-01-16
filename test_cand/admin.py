from django.contrib import admin
from .models import TestCand, CandEdu, CandExp


admin.site.register([TestCand, CandEdu, CandExp])
