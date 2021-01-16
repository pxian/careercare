from django.db import models


class TestCand(models.Model):
    name = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    skills = models.CharField(max_length=100, null=True, blank=True)
    link = models.CharField(max_length=100, null=True, blank=True)
    preferred_location = models.CharField(
        max_length=100, null=True, blank=True)
    expected_salary = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class CandExp(models.Model):
    cand = models.ForeignKey('TestCand', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=500, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    duration = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.cand_id)


class CandEdu(models.Model):
    cand = models.ForeignKey('TestCand', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True)
    school = models.CharField(max_length=500, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    duration = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.cand_id)
