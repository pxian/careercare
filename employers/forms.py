from django import forms
from .models import Employer, User, Individual
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


INDUSTRY = [
    ('Accounting/Finance', 'Accounting/Finance'),
    ('Admin/Human Resources', 'Admin/Human Resources'),
    ('Arts/Media/Communications', 'Arts/Media/Communications'),
    ('Computer/Information Technology', 'Computer/Information Technology'),
    ('Education/Training', 'Education/Training'),
    ('Engineering', 'Engineering'),
    ('Entertainment/Media', 'Entertainment/Media'),
    ('Healthcare', 'Healthcare'),
    ('Hotel/Restaurant', 'Hotel/Restaurant'),
    ('Manufacturing/Production', 'Manufacturing/Production'),
    ('Sales/Marketing', 'Sales/Marketing'),
    ('Sciences', 'Sciences'),
    ('Services', 'Services'),
    ('Others', 'Others'),
]

EMPLOYEES = [
    ('1 - 50 Employees', '1 - 50 Employees'),
    ('51 - 200 Employees', '51 - 200 Employees'),
    ('201 - 500 Employees', '201 - 500 Employees'),
    ('501 - 1000 Employees', '501 - 1000 Employees'),
    ('1001 - 2000 Employees', '1001 - 2000 Employees'),
    ('2001 - 5000 Employees', '2001 - 5000 Employees'),
    ('More than 5000 Employees', 'More than 5000 Employees'),
]


STATES = [
    ('Perlis', 'Perlis'),
    ('Perak', 'Perak'),
    ('Johor', 'Johor'),
    ('Sabah', 'Sabah'),
    ('Kedah', 'Kedah'),
    ('Melaka', 'Melaka'),
    ('Pahang', 'Pahang'),
    ('Penang', 'Penang'),
    ('Sarawak', 'Sarawak'),
    ('Kelantan', 'Kelantan'),
    ('Selangor', 'Selangor'),
    ('Terengganu', 'Terengganun'),
    ('Kuala Lumpur', 'Kuala Lumpur'),
    ('Negeri Sembilan', 'Negeri Sembilan'),
]


class SignUpForm(UserCreationForm):
    role = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'password1', 'password2', 'role')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control w-75', 'placeholder': 'First Name', 'required': 'True'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control w-75', 'placeholder': 'Last Name', 'required': 'True'}),
            'username': forms.TextInput(attrs={'class': 'form-control w-75', 'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'class': 'form-control w-75', 'placeholder': 'Email', 'required': 'True'}),
        }


class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ('name', 'industry', 'address_1', 'address_2',
                  'state', 'city', 'pcode', 'size', 'website')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control w-75', 'required': 'True'}),
            'size': forms.Select(choices=EMPLOYEES, attrs={'class': 'custom-select w-75', 'required': 'True'}),
            'website': forms.TextInput(attrs={'class': 'form-control w-75', 'required': 'True'}),
            'industry': forms.Select(choices=INDUSTRY, attrs={'class': 'custom-select w-75', 'required': 'True'}),
            'address_1': forms.TextInput(attrs={'class': 'form-control w-75', 'required': 'True', 'placeholder': 'Address Line 1'}),
            'address_2': forms.TextInput(attrs={'class': 'form-control w-75', 'placeholder': 'Address Line 2'}),
            'state': forms.Select(choices=STATES, attrs={'class': 'custom-select w-75', 'required': 'True'}),
            'city': forms.TextInput(attrs={'class': 'form-control w-75', 'placeholder': 'City'}),
            'pcode': forms.TextInput(attrs={'class': 'form-control w-75', 'required': 'True', 'placeholder': 'Postal Code'}),
        }


class IndividualForm(forms.ModelForm):
    class Meta:
        model = Individual
        fields = ('phone_number', 'address_1',
                  'address_2', 'state', 'city', 'pcode')
        widgets = {
            'address_1': forms.TextInput(attrs={'class': 'form-control w-75', 'required': 'True', 'placeholder': 'Address Line 1'}),
            'address_2': forms.TextInput(attrs={'class': 'form-control w-75', 'placeholder': 'Address Line 2'}),
            'state': forms.Select(choices=STATES, attrs={'class': 'custom-select w-75', 'required': 'True'}),
            'city': forms.TextInput(attrs={'class': 'form-control w-75', 'placeholder': 'City'}),
            'pcode': forms.TextInput(attrs={'class': 'form-control w-75', 'required': 'True', 'placeholder': 'Postal Code'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control w-75'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control w-75'}),
            'username': forms.TextInput(attrs={'class': 'form-control w-75'}),
            'email': forms.TextInput(attrs={'class': 'form-control w-75'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Individual
        fields = ('phone_number', 'address_1',
                  'address_2', 'state', 'city', 'pcode')
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control W-75', 'style': 'min-width: 226px !important'}),
            'address_1': forms.TextInput(attrs={'class': 'form-control w-75', 'required': 'True'}),
            'address_2': forms.TextInput(attrs={'class': 'form-control w-75'}),
            'state': forms.Select(choices=STATES, attrs={'class': 'custom-select w-75', 'required': 'True'}),
            'city': forms.TextInput(attrs={'class': 'form-control w-75'}),
            'pcode': forms.TextInput(attrs={'class': 'form-control w-75', 'required': 'True'}),
        }
