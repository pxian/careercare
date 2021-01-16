from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from .models import Employer, User, Individual
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate, update_session_auth_hash
from .forms import SignUpForm, EmployerForm, IndividualForm, ProfileForm, ContactForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            get_user = User.objects.last()
            if request.POST['role'] == "employers":
                employer_group = Group.objects.get(name='Employers')
                employer_group.user_set.add(get_user)
                user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
                auth_login(request, user)
                return redirect('employers:welcome')
            else:
                individual_group = Group.objects.get(name='Individual')
                individual_group.user_set.add(get_user)
                user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
                auth_login(request, user)
                return redirect('employers:welcome')
    else:
        form = SignUpForm()
    return render(request, 'employers/signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('dashboard:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'employers/login.html', {'form': form})


def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('employers:login')


def welcome(request):
    user = User.objects.last()
    group = user.groups.last()
    if request.method == 'POST':
        if group.id == 1:
            form = EmployerForm(request.POST)
            obj = Employer.objects.filter(name=request.POST['name']).exists()
            if request.POST['pcode'].isdigit():
                if obj is True:
                    messages.error(request, "Company already registered.")
                else:
                    obj = Employer.objects.create(
                        user_id=request.user.id,
                        name=request.POST['name'],
                        industry=request.POST['industry'],
                        address_1=request.POST['address_1'],
                        address_2=request.POST['address_2'],
                        state=request.POST['state'],
                        pcode=request.POST['pcode'],
                        size=request.POST['size'],
                        website=request.POST['website']),
                    return redirect('dashboard:dashboard')
            else:
                form = EmployerForm()
                messages.error(request, "Please provide a valid postal code.")
        else:
            form = IndividualForm(request.POST)
            obj = Individual.objects.filter(
                phone_number=request.POST['phone_number']).exists()
            if request.POST['pcode'].isdigit() and request.POST['phone_number'].isdigit():
                if obj is True:
                    messages.error(request, "Phone number already registered.")
                else:
                    obj = Individual.objects.create(
                        user_id=request.user.id,
                        address_1=request.POST['address_1'],
                        address_2=request.POST['address_2'],
                        state=request.POST['state'],
                        pcode=request.POST['pcode'],
                        phone_number=request.POST['phone_number']),
                    return redirect('dashboard:dashboard')
            else:
                form = IndividualForm()
                messages.error(request, "Invalid postal code or phone number.")
    else:
        if group.id == 1:
            form = EmployerForm()
        else:
            form = IndividualForm()
    return render(request, 'employers/welcome.html', {'form': form, 'group': group})


def profile(request):
    group = str(request.user.groups.get())
    obj = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=obj)
        if form.is_valid() and form.has_changed():
            form.save()
            messages.success(request, "Record was updated successfully!")
            return redirect('employers:profile')
        else:
            messages.error(request, "You did not make any changes.")
            return redirect('employers:profile')
    else:
        form = ProfileForm(instance=obj)
        if group == "Employers":
            employer = Employer.objects.values().get(user_id=request.user.id)
            return render(request, 'employers/profile.html', {'form': form, 'obj': obj, 'employer': employer, 'group': group})
        else:
            individual = Individual.objects.values().get(user_id=request.user.id)
            return render(request, 'employers/profile.html', {'form': form, 'obj': obj, 'individual': individual, 'group': group})


def password(request):
    group = str(request.user.groups.get())
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid() and form.has_changed():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(
                request, "Password has been changed successfully!")
            return redirect('employers:password')
        else:
            messages.error(request, "You did not make any changes.")
            return redirect('employers:password')
    else:
        form = PasswordChangeForm(user=request.user)
        if group == "Employers":
            employer = Employer.objects.values().get(user_id=request.user.id)
            return render(request, 'employers/password.html', {'form': form, 'employer': employer, 'group': group})
        else:
            individual = Individual.objects.values().get(user_id=request.user.id)
            return render(request, 'employers/password.html', {'form': form, 'individual': individual, 'group': group})


def company(request):
    obj = Employer.objects.get(user_id=request.user.id)
    group = str(request.user.groups.get())
    if request.method == 'POST':
        form = EmployerForm(request.POST, instance=obj)
        if form.is_valid() and form.has_changed():
            if request.POST['pcode'].isdigit():
                form.save()
                messages.success(request, "Record was updated successfully!")
                return redirect('employers:company')
            else:
                messages.error(request, "Invalid postal code or phone number.")
                return redirect('employers:company')
        else:
            messages.error(request, "You did not make any changes.")
            return redirect('employers:company')
    else:
        form = EmployerForm(instance=obj)
        employer = Employer.objects.values().get(user_id=request.user.id)
    return render(request, 'employers/company.html', {'form': form, 'obj': obj, 'employer': employer, 'group': group})


def contact(request):
    obj = Individual.objects.get(user_id=request.user.id)
    group = str(request.user.groups.get())
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=obj)
        if form.is_valid() and form.has_changed():
            if request.POST['pcode'].isdigit() and request.POST['phone_number'].isdigit():
                form.save()
                messages.success(request, "Record was updated successfully!")
                return redirect('employers:contact')
            else:
                messages.error(request, "Invalid postal code or phone number.")
                return redirect('employers:contact')
        else:
            messages.error(request, "You did not make any changes.")
            return redirect('employers:contact')
    else:
        form = ContactForm(instance=obj)
        individual = Individual.objects.values().get(user_id=request.user.id)
    return render(request, 'employers/contact.html', {'form': form, 'obj': obj, 'individual': individual, 'group': group})


def deleteaccount(request):
    obj = User.objects.filter(id=request.user.id)
    if request.method == 'POST':
        obj.delete()
    return JsonResponse(serializers.serialize('json', obj), safe=False)
