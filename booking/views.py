import re
from .models import Booking
from django.apps import apps
from datetime import datetime
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import BookingForm, CancellationForm
from django.contrib.auth.decorators import login_required


# @login_required(login_url='/employers/login/')
def booking(request):
    queryset_array = list()
    Service = apps.get_model('service', 'Service')
    booking = Booking.objects.filter(
        user_id=request.user.id).order_by("booked_date")
    details = Service.objects.filter(
        booking__in=Booking.objects.filter(user_id=request.user.id)).order_by("booking__booked_date")
    now = datetime.now().date()
    for i in zip(booking, details):
        queryset_array.append(i)
    if not queryset_array:
        return render(request, 'booking/booking.html')
    return render(request, 'booking/booking.html', {'queryset_array': queryset_array, 'booking': booking, 'now': now})


def service(request, id):
    Service = apps.get_model('service', 'Service')
    details = Service.objects.get(id=id)
    return render(request, 'booking/service.html', {'details': details})


def formatstring(details):
    get_words = re.findall(r"[\w']+|[.,!?;]+|[\n']", details)
    return get_words


def bookservice(request, id):
    Individual = apps.get_model('employers', 'Individual')
    individual = Individual.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        convert_date = datetime.strptime(
            request.POST['booked_date'], '%m/%d/%Y')
        if request.POST['newaddress'] != individual.address_1:
            obj = Booking.objects.create(
                user_id=request.user.id,
                service_id=id,
                booked_date=convert_date.date(),
                booked_time=request.POST['booked_time'],
                address=request.POST['newaddress'],
                additional_info=request.POST['additional_info'])
        messages.success(request, "Booking has been made successfully!")
        return redirect('booking:booking')
    else:
        form = BookingForm()
        Service = apps.get_model('service', 'Service')
        details = Service.objects.get(id=id)
        return render(request, 'booking/bookservice.html', {'form': form, 'details': details, 'individual': individual})


def markcomplete(request, id):
    obj = Booking.objects.filter(id=id)
    if request.method == 'POST':
        for i in obj:
            i.job_status = "Complete"
            i.save()
        return JsonResponse(serializers.serialize('json', obj), safe=False)


def deletebooking(request, id):
    obj = Booking.objects.filter(id=id)
    if request.method == 'POST':
        for i in obj:
            i.hidden = "True"
            i.save()
        return JsonResponse(serializers.serialize('json', obj), safe=False)


def complete(request, id):
    booking = Booking.objects.get(id=id)
    Service = apps.get_model('service', 'Service')
    details = Service.objects.get(id=booking.service_id)
    Individual = apps.get_model('employers', 'Individual')
    individual = Individual.objects.get(user_id=request.user.id)
    d_address = [[details.address_1], [details.address_2],
                 [details.pcode], [details.city], [details.state]]
    i_address = [[individual.address_1], [individual.address_2], [
        individual.pcode], [individual.city], [individual.state]]
    if booking.address:
        b_address = formataddress(booking.address)
        return render(request, 'booking/complete.html', {'booking': booking, 'details': details, 'individual': individual, 'd_address': d_address, 'b_address': b_address})
    else:
        return render(request, 'booking/complete.html', {'booking': booking, 'details': details, 'individual': individual, 'd_address': d_address, 'i_address': i_address})


def upcoming(request, id):
    booking = Booking.objects.get(id=id)
    Service = apps.get_model('service', 'Service')
    details = Service.objects.get(id=booking.service_id)
    Individual = apps.get_model('employers', 'Individual')
    individual = Individual.objects.get(user_id=request.user.id)
    d_address = [[details.address_1], [details.address_2],
                 [details.pcode], [details.city], [details.state]]
    i_address = [[individual.address_1], [individual.address_2], [
        individual.pcode], [individual.city], [individual.state]]
    remaining = caldays(booking)
    if booking.address:
        b_address = formataddress(booking.address)
        return render(request, 'booking/upcoming.html', {'booking': booking, 'details': details, 'individual': individual, 'd_address': d_address, 'b_address': b_address, 'remaining': remaining})
    else:
        return render(request, 'booking/upcoming.html', {'booking': booking, 'details': details, 'individual': individual, 'd_address': d_address, 'i_address': i_address, 'remaining': remaining})


def formataddress(address):
    if address.count(', ') == 5:
        temp = address.split(", ", 3)[:3]
        line1 = ", ".join(temp)
        line2 = address.split(", ", 3)[3]
        return line1, line2
    elif address.count(', ') == 4:
        temp = address.split(", ", 2)[:2]
        line1 = ", ".join(temp)
        line2 = address.split(", ", 2)[2]
        return line1, line2
    else:
        temp = address.split(", ", 1)[:1]
        line1 = ", ".join(temp)
        line2 = address.split(", ", 1)[1]
        return line1, line2


def caldays(booking):
    now = datetime.now().date()
    temp = booking.booked_date - now
    return temp.days


def cancelbooking(request, id):
    booking = Booking.objects.get(id=id)
    if request.method == 'POST':
        if request.POST['other_reasons']:
            booking.reasons = request.POST['other_reasons']
            booking.job_status = "Cancelled"
            booking.save()
        else:
            booking.reasons = request.POST['reasons']
            booking.job_status = "Cancelled"
            booking.save()
        messages.success(request, "Record was updated successfully!")
        return redirect('booking:booking')
    else:
        form = CancellationForm()
        return render(request, 'booking/cancellation.html', {'form': form, 'booking': booking})
