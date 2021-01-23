from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Employee, Freelancer, User, Employee_Edu,Employee_Exp
from django.forms import ModelForm
from django.conf import settings
from django.forms import modelformset_factory

GROUP_CHOICES = (
    ('employee','Full Time Job'),
    ('freelancer','Freelancer'),
)


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
	    model = User
	    fields = ["username", "email", "password1", "password2"]

class ProfileForm(forms.ModelForm):
    resume = forms.FileField(
        required=False,
        label='Select a file',
        help_text='max. 42 megabytes'
    )
    class Meta:
        model = Employee
        fields = (
            
            'name',
            'phone_Number',
            'nationality', 
            'address',
            'city',         
            'skills',
            'languages',
            'prefered_work_location',
            'expected_salary',
            'resume',
            'part_time',
            'full_time',
            )

EduFormSet = modelformset_factory(
    Employee_Edu,
    extra=1,
    max_num=1,
    fields=('university',
                'university_location',
                'graduation_date',
                'qualification',
                'field_of_study',
                'title','grade',),
                
                )

ExpFormSet = modelformset_factory(
    Employee_Exp,
    extra=1,
    max_num=1,
    fields=('position_title',
            'company_name',
            'country',
            'state',
            'duration',
            'specialization',
            'industry',
            'position_level',
            'description',),
)




class FreeForm(forms.ModelForm):
    class Meta:
        model = Freelancer
        fields = ('contact_person_name','registered_business_name','registration_number','address','phone_Number','category','service_type','services_offer','description','city')

    # def __init__(self,user,*args,**kwargs):
    #     self.user=user.profile

