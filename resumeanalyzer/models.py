import os
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Create your models here.
class FailOnDuplicateFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        return name

    def _save(self, name, content):
        if self.exists(name):
            raise ValidationError('File already exists: %s' % name)
        return super(FailOnDuplicateFileSystemStorage, self)._save(name, content)


class JobDesc(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    jobid = models.AutoField(primary_key=True)
    jobdesc = models.FileField('Upload Job Description', upload_to='jobdesc/', null=False, blank=False, unique=True, storage=FailOnDuplicateFileSystemStorage())
    title = models.CharField('Title', max_length=250, null=False, blank=False)
    summary = models.CharField('Summary', max_length=10000, null=True, blank=True)
    uploaded_on = models.DateTimeField('Uploaded On', auto_now_add=True)


    def extension(self):
        return os.path.splitext(self.jobdesc.name)[1][1:].strip().lower()


    def delete(self, *args, **kwargs):
        self.jobdesc.delete()
        super().delete(*args, **kwargs)


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resumeid = models.AutoField(primary_key=True)
    resume = models.FileField('Upload Resumes', upload_to='resumes/', null=False, blank=False, unique=True, storage=FailOnDuplicateFileSystemStorage())
    name = models.CharField('Name', max_length=1000, null=True, blank=True, unique=True)
    email = models.CharField('Email', max_length=1000, null=True, blank=True)
    mobile_number = models.CharField('Mobile Number',  max_length=255, null=True, blank=True)
    summary = models.CharField('Summary', max_length=10000, null=True, blank=True)
    education = models.CharField('Education', max_length=255, null=True, blank=True)
    skills = models.CharField('Skills', max_length=10000, null=True, blank=True)
    company_name = models.CharField('Company Name', max_length=10000, null=True, blank=True)
    designation = models.CharField('Designation', max_length=10000, null=True, blank=True)
    experience = models.CharField('Experience', max_length=10000, null=True, blank=True)
    uploaded_on = models.DateTimeField('Uploaded On', auto_now_add=True)
    STATUS = (
        ('Available', 'Available'),
        ('Shortlisted', 'Shortlisted'),
        )
    status = models.CharField(max_length=20, choices=STATUS, default='Available')
    note = models.CharField('Note', max_length=10000, null=True, blank=True)


    def shortlist(self):
        self.status = 'Shortlisted'
        self.save()


    def delist(self):
        self.status = 'Available'
        self.save()


    def extension(self):
        return os.path.splitext(self.resume.name)[1][1:].strip().lower()


    def delete(self, *args, **kwargs):
        self.resume.delete()
        super().delete(*args, **kwargs)


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    jobid = models.ForeignKey(JobDesc, on_delete=models.CASCADE)
    resumeid = models.ForeignKey(Resume, on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)