from django import forms
from .models import JobDesc, Resume
from django.forms import ClearableFileInput, FileInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['resume', 'name', 'email', 'mobile_number', 'summary', 'education', 'skills', 'company_name', 'designation', 'experience', 'note']
        widgets = {'resume': ClearableFileInput(attrs={'multiple': True}), 'resume': FileInput(
            attrs={'accept': 'application/pdf, application/vnd.openxmlformats-officedocument.wordprocessingml.document'})}
    
# delete the resume files associated with each object or record
@receiver(post_delete, sender=Resume)
def resume_delete(sender, instance, **kwargs):
    instance.resume.delete(False)


class JobDescForm(forms.ModelForm):
    class Meta:
        model = JobDesc
        fields = ['jobdesc','title', 'summary']
        widgets = {'jobdesc': ClearableFileInput(attrs={'multiple': False}), 'jobdesc': FileInput(
            attrs={'accept': 'application/pdf, application/vnd.openxmlformats-officedocument.wordprocessingml.document'})}

# delete the jobdesc files associated with each object or record
@receiver(post_delete, sender=JobDesc)
def job_delete(sender, instance, **kwargs):
    instance.jobdesc.delete(False)


FILTER= [
    ('all', 'all'),
    ('shortlisted', 'shortlisted'),
    ]

class Filter(forms.Form):
    filter = forms.CharField(widget=forms.RadioSelect(choices=FILTER))
