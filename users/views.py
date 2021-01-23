from django.shortcuts import render, redirect
from django.core import serializers
from django.http import JsonResponse
from .forms import RegisterForm, FreeForm
from django.contrib import messages
from .models import Employee,User,Freelancer, Employee_Edu, Employee_Exp
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import Group
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from datetime import datetime
from users.forms import (ProfileForm)
from .forms import ExpFormSet,EduFormSet
from django.forms import formset_factory
from django.contrib.auth import update_session_auth_hash
from django.forms.models import modelformset_factory

# from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            get_user = User.objects.last()
            user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )

            auth_login(request, user)
            return redirect('users:create_profile')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def log_in(request):
    
    if request.method == 'POST':
        log_in_form = AuthenticationForm(data=request.POST)
        if log_in_form.is_valid():
            user = log_in_form.get_user()
            auth_login(request, user)
            return redirect('insights:insights')
    else:
        log_in_form = AuthenticationForm()
        return render(request, 'login.html', {'form': log_in_form})


def log_out(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('home:home')

def create_profile(request):
    user = User.objects.last()
    # EduFormSet= formset_factory(EduForm)
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES)
        formset = EduFormSet(request.POST,prefix='edufs')
        expformset = ExpFormSet(request.POST,prefix='expfs')
        obj = Employee.objects.create(user_id = request.user.id, 
                                    name = request.POST['name'],
                                    phone_Number = request.POST['phone_Number'],
                                    nationality = request.POST['nationality'],
                                    address = request.POST['address'],
                                    city = request.POST['city'],
                                    skills = request.POST['skills'],
                                    languages = request.POST['languages'],
                                    prefered_work_location = request.POST['prefered_work_location'],
                                    resume = request.FILES['resume']),
        for form in expformset:
            exp = form.save(commit=False)
            exp.user_id = request.user.id
            exp.save()
        for form in formset: 
            edu =form.save(commit=False)
            edu.user_id = request.user.id
            edu.save()
            
        return redirect('home:userhome')

    else:
        form = ProfileForm()
        formset = EduFormSet(queryset=Employee_Edu.objects.none(),prefix='edufs')
        expformset = ExpFormSet(queryset=Employee_Exp.objects.none(),prefix='expfs')


    context = {
    'profile_form' : ProfileForm(),
    'formset' : EduFormSet(queryset=Employee_Edu.objects.none(),prefix='edufs'),
    'expformset' : ExpFormSet(queryset=Employee_Exp.objects.none(),prefix='expfs'),
}
    return render(request, 'users/create_profile.html', context)




# @login_required
def edit_profile(request):
    user = User.objects.last()

    if request.method == 'POST':
        obj = Employee.objects.get(user_id=request.user.id)
        obj_edu = Employee_Edu.objects.filter(user_id=request.user.id)
        obj_exp = Employee_Exp.objects.filter(user_id=request.user.id)
        profileform =ProfileForm(request.POST,request.FILES,instance=obj)
        eduformset = EduFormSet(request.POST)
        expformset = ExpFormSet(request.POST)
        if profileform.is_valid() and profileform.has_changed():
            profileform.save()                   
            return redirect('users:edit_profile')
        else:
            return redirect('users:edit_profile')
        if eduformset.is_valid() and eduformset.has_changed():
            for form in eduformset:
                edu = form.save()
                edu.user_id= request.user.id
                edu.save()    
            return redirect('users:edit_profile')
        else:    
            messages.error(request, "You did not make any changes.")
            return redirect('users:edit_profile')
        if expformset.is_valid() and expformset.has_changed():
            for form in expformset:
                exp = form.save()
                exp.user_id = request.user.id
                exp.save()                                      
            return redirect('users:edit_profile')
        else:    
            messages.error(request, "You did not make any changes.")
            return redirect('users:edit_profile')
            # if profileform.is_valid() and eduformset.is_valid() and expformset.is_valid():
            #     if profileform.has_changed() or eduformset.has_changed() or expformset.has_changed():
            #         profileform.save()
            #         instances = eduformset.save(commit=False)
            #         for instance in instances:
            #             instance.user = request.user.id
            #             instance.save()
            #         instancess = expformset.save(commit=False)
            #         for instance in instancess:
            #             instance.user = request.user.id
            #             instance.save()
            #         eduformset.save()
            #         expformset.save()
            #         messages.success(request, "Record was updated successfully!")
            #         return redirect('users:edit_profile')
            # if form.is_valid() and form.has_changed():
            #     form.save()
            #     messages.success(request, "Record was updated successfully!")
            #     return redirect('users:edit_profile')
            #     else:
    
            #         messages.error(request, "You did not make any changes.")
            #         return redirect('users:edit_profile')
            # else:
            #     return redirect('users:edit_profile')

    else:
 
        obj = Employee.objects.get(user_id=request.user.id)
        obj_edu = Employee_Edu.objects.filter(user_id=request.user.id)
        obj_exp = Employee_Exp.objects.filter(user_id=request.user.id)
        # obj_edu = Employee_Edu.objects.filter(user_id=request.user.id)
        # obj_exp = Employee_Exp.objects.filter(user_id=request.user.id)
        profileform = ProfileForm(instance=obj)
        eduformset = EduFormSet()
        expformset = ExpFormSet()
        
        employee = Employee.objects.values().get(user_id=request.user.id)
        employee_edu = Employee_Edu.objects.values().filter(user_id=request.user.id)
        employee_exp = Employee_Exp.objects.values().filter(user_id=request.user.id)
        context = {
        'profileform' : profileform,
        'obj':obj,
        'eduformset' : EduFormSet(prefix='edufs'),
        'expformset' : ExpFormSet(prefix='expfs'),
        'employee':employee,
        'employee_edu':employee_edu,
        'employee_exp':employee_exp,
            }
        return render(request,'users/edit_profile.html',context)
    
    