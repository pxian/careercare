from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=100, null=True)
    service_type = models.CharField(max_length=100, null=True)
    duration = models.CharField(max_length=100, null=True)
    jobs_completed = models.IntegerField(null=True, default=0)
    description = models.TextField(null=True)
    service_offer = models.TextField(null=True)
    rating = models.IntegerField(null=True)
    contact_person = models.CharField(max_length=100, null=True)
    address_1 = models.CharField(max_length=500, null=True, blank=True)
    address_2 = models.CharField(max_length=500, null=True, blank=True)
    state = models.CharField(max_length=500, null=True, blank=True)
    city = models.CharField(max_length=500, null=True, blank=True)
    pcode = models.CharField(max_length=500, null=True, blank=True)
    registration_no = models.CharField(max_length=100, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.contact_person
