from django import forms
from .models import Booking


REASONS = [
    ('Change of plans', 'Change of plans'),
    ('I no longer need it', 'I no longer need it'),
    ('Quality was less than I expected', 'Quality was less than I expected'),
    ('Poor attitude of service provider', 'Poor attitude of service provider'),
    ('Others', 'Others'),
]


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('booked_date', 'booked_time', 'additional_info')
        widgets = {
            'booked_date': forms.TextInput(attrs={'class': 'form-control w-100', 'data-provide': 'datepicker', 'placeholder': 'Date', 'requried': 'True'}),
            'booked_time': forms.TextInput(attrs={'class': 'form-control w-100', 'id': 'id_booked_time', 'placeholder': 'Time', 'requried': 'True'}),
            'additional_info': forms.Textarea(attrs={'class': 'form-control w-100 p-3', 'placeholder': 'Please state if you have any requests', 'style': 'height: 100px !important'}),
        }


class CancellationForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('reasons',)
        widgets = {
            'reasons': forms.RadioSelect(choices=REASONS, attrs={'class': 'list-unstyled', 'onclick': 'showInput()', 'requried': 'True'}),
        }
