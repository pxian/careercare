from django import forms
from .models import JobAd, Invitation


TYPE = [
    ('Full-Time', 'Full-Time'),
    ('Part-Time', 'Part-Time'),
    ('Contract', 'Contract'),
]

LEVELS = [
    ('Non-Executive', 'Non-Executive'),
    ('Entry Level', 'Entry Level'),
    ('Junior Executive', 'Junior Executive'),
    ('Senior Executive', 'Senior Executive'),
    ('Manager', 'Manager'),
    ('Senior Manager', 'Senior Manager'),
]

SPEC = [
    ('Accounting/Finance', 'Accounting/Finance'),
    ('Admin/Human Resources', 'Admin/Human Resources'),
    ('Arts/Media/Communications', 'Arts/Media/Communications'),
    ('Computer/IT', 'Computer/IT'),
    ('Education/Training', 'Education/Training'),
    ('Engineering', 'Engineering'),
    ('Healthcare', 'Healthcare'),
    ('Hotel/Restaurant', 'Hotel/Restaurant'),
    ('Sales/Marketing', 'Sales/Marketing'),
    ('Sciences', 'Sciences'),
    ('Services', 'Services'),
    ('Others', 'Others'),
]

STATES = [
    ('Johor', 'Johor'),
    ('Kedah', 'Kedah'),
    ('Kelantan', 'Kelantan'),
    ('Kuala Lumpur', 'Kuala Lumpur'),
    ('Melaka', 'Melaka'),
    ('Negeri Sembilan', 'Negeri Sembilan'),
    ('Pahang', 'Pahang'),
    ('Penang', 'Penang'),
    ('Perak', 'Perak'),
    ('Perlis', 'Perlis'),
    ('Sabah', 'Sabah'),
    ('Sarawak', 'Sarawak'),
    ('Selangor', 'Selangor'),
    ('Terengganu', 'Terengganu'),
]


class JobAdForm(forms.ModelForm):
    class Meta:
        model = JobAd
        fields = ('position_title', 'employment_type', 'position_level', 'job_specialization',
                  'job_description', 'job_requirements', 'location', 'min_salary', 'max_salary', 'closing_date')
        widgets = {
            'position_title': forms.TextInput(attrs={'class': 'form-control'}),
            'employment_type': forms.Select(choices=TYPE, attrs={'class': 'custom-select'}),
            'position_level': forms.Select(choices=LEVELS, attrs={'class': 'custom-select'}),
            'job_specialization': forms.Select(choices=SPEC, attrs={'class': 'custom-select'}),
            'job_description': forms.Textarea(attrs={'class': 'form-control'}),
            'job_requirements': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.Select(choices=STATES, attrs={'class': 'custom-select'}),
            'min_salary': forms.TextInput(attrs={'class': 'form-control mr-3', 'placeholder': 'Minimum'}),
            'max_salary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Maximum'}),
            'closing_date': forms.TextInput(attrs={'class': 'form-control', 'data-provide': 'datepicker'}),
        }


class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ('booked_date', 'booked_time', 'messages')
        widgets = {
            'booked_date': forms.TextInput(attrs={'class': 'form-control w-100', 'data-provide': 'datepicker', 'placeholder': 'Date', 'required': 'True'}),
            'booked_time': forms.TextInput(attrs={'class': 'form-control w-100', 'id': 'id_booked_time', 'placeholder': 'Time', 'required': 'True'}),
            'messages': forms.Textarea(attrs={'class': 'form-control w-100 p-3', 'placeholder': 'Your message', 'style': 'height: 200px !important', 'required': 'True'}),
        }
