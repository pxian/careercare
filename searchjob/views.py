from django.shortcuts import render,redirect
import string
from django.apps import apps
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
import re
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def search(request):
    results = fullsearch(request)
    if results:
        if results[3] == "pos":
            queryset_array = results[0]
            position_title = results[1]
            return render(request, 'searchjob/fullsearch.html', {'queryset_array': queryset_array, 'position_title': position_title})
        elif results[3] == "poscity":
            queryset_array = results[0]
            position_title = results[1]
            city = results[2]
            return render(request, 'searchjob/fullsearch.html', {'queryset_array': queryset_array, 'position_title': position_title, 'city': city})
        elif results[3] == "posspec":
            queryset_array = results[0]
            position_title = results[1]
            job_specialization = results[2]
            return render(request, 'searchjob/fullsearch.html', {'queryset_array': queryset_array, 'position_title': position_title, 'job_specialization': job_specialization})
        # elif results[3] == "cities":
        #     queryset_array = results[0]
        #     city = results[1]
        #     return render(request,'searchjob/fullsearch.html',{'queryset_array':queryset_array,'city':city})
        # elif results[3] == "cityjob":
        #     queryset_array = results[0]
        #     city = results[1]
        #     job_specialization = results[2]
        #     return render(request,'searchjob/fullsearch.html',{'queryset_array':queryset_array,'city':city,'job_specialization':job_specialization})
        # elif results[3] == "job":
        #     queryset_array = results[0]
        #     job_specialization = results[1]
        #     return render(request,'searchjob/fullsearch.htm',{'queryset_array':queryset_array,'job_specialization':job_specialization})
        else:
            queryset_array = results[0]
            position_title = results[1]
            city = results[2]
            job_specialization = results[3]
            return render(request, 'searchjob/fullsearch.html', {'queryset_array': queryset_array, 'position_title': position_title, 'city': city, 'job_specialization': job_specialization})
    else:
        jobs = JobAd.objects.all()
        return render(request, 'searchjob/fullsearch.html',{'jobs':jobs})

def fsearch(request):
    results = freesearch(request)
    if results:
        if results[3] == "pos":
            queryset_array = results[0]
            job_title = results[1]
            return render(request, 'searchjob/freesearch.html', {'queryset_array': queryset_array, 'job_title': job_title})
        elif results[3] == "poscity":
            queryset_array = results[0]
            job_title = results[1]
            city = results[2]
            return render(request, 'searchjob/freesearch.html', {'queryset_array': queryset_array, 'job_title': job_title, 'city': city})
        elif results[3] == "postype":
            queryset_array = results[0]
            job_title = results[1]
            job_type = results[2]
            return render(request, 'searchjob/freesearch.html', {'queryset_array': queryset_array, 'job_title': job_title, 'job_type': job_type})
        else:
            queryset_array = results[0]
            job_title = results[1]
            city = results[2]
            job_type = results[3]
            return render(request, 'searchjob/freesearch.html', {'queryset_array': queryset_array, 'job_title': job_title, 'city': city, 'job_type': job_type})
    else:
        jobs = Freelance.objects.all()
        return render(request, 'searchjob/freesearch.html',{'jobs':jobs})

def freesearch(request):
    queryset = Freelance.objects.all()
    job_title = request.GET.get('job_title')
    city = request.GET.get('city')
    job_type = request.GET.get('job_type')
    if job_title:
        queryset_array = freesingle(formatstring(
            job_title), queryset, "job_title")
        if city and job_type:
            if city:
                queryset_array = freemultiple(
                    queryset_array, formatstring(city), "city")
                if job_type:
                    queryset_array = freemultiple(
                        queryset_array, formatstring(job_type), "job_type")
        else:
            if city:
                queryset_array = freemultiple(
                    queryset_array, formatstring(city), "city")
                return queryset_array, job_title, city, "poscity"
            elif job_type:
                queryset_array = freemultiple(
                    queryset_array, formatstring(job_type), "job_type")
                return queryset_array, job_title, job_type, "postype"
            else:
                queryset_array = freesingle(formatstring(
                    job_title), queryset, "job_title")
                return queryset_array, job_title,"", "pos"
        return queryset_array, job_title, city, job_type

def freesingle(value1, queryset, label):
    queryset_array = list()
    if label == "job_title":
        for i in value1:
            results = queryset.filter(job_title__icontains=i)
            if results:
                queryset_array.append(results)
        return queryset_array
    elif label == "city":
        for i in value1:
            results = queryset.filter(city__icontains=i)
            if results:
                queryset_array.append(results)
        return queryset_array
    elif label == "job_type":
        for i in value1:
            results = queryset.filter(job_type__icontains=i)
            if results:
                queryset_array.append(results)
        return queryset_array
    else:
        results = queryset.filter(category=value1)
        queryset_array.append(results)
    return queryset_array

def freemultiple(queryset, value2, label):
    queryset_array = list()
    if label == "city":
        for i in queryset:
            for j in value2:
                results = i.filter(city__icontains=j)
                if results:
                    queryset_array.append(results)
        return queryset_array
    elif label == "job_type":
        for i in queryset:
            for j in value2:
                results = i.filter(job_type__icontains=j)
                if results:
                    queryset_array.append(results)
        return queryset_array

def fullsearch(request):
    queryset = JobAd.objects.all()
    position_title = request.GET.get('position_title')
    city = request.GET.get('location')
    job_specialization = request.GET.get('job_specialization')
    if position_title:
        queryset_array = single(formatstring(
            position_title), queryset, "position_title")
        if city and job_specialization:
            if city:
                queryset_array = multiple(
                    queryset_array, formatstring(city), "city")
                if job_specialization:
                    queryset_array = multiple(
                        queryset_array, formatstring(job_specialization), "job_specialization")
        else:
            if city:
                queryset_array = multiple(
                    queryset_array, formatstring(city), "city")
                return queryset_array, position_title, city, "poscity"
            elif job_specialization:
                queryset_array = multiple(
                    queryset_array, formatstring(job_specialization), "job_specialization")
                return queryset_array, position_title, job_specialization, "posspec"
            else:
                queryset_array = single(formatstring(
                    position_title), queryset, "position_title")
                return queryset_array, position_title,"", "pos"
        return queryset_array, position_title, city, job_specialization
    # elif city:
    #     queryset_array = single(formatstring(
    #         city), queryset, "city")
    #     if job_specialization:
    #         queryset_array = multiple(
    #                     queryset_array, formatstring(job_specialization), "job_specialization")
    #         return queryset_array, city, job_specialization,"cityjob"
    #     elif city:
    #         queryset_array = single(formatstring(
    #                 city), queryset, "city")
    #         return queryset_array, position_title, "cities"
    # elif job_specialization:
    #     queryset_array = single(formatstring(
    #         job_specialization), queryset, "job_specialization")
    #     return queryset_array,job_specialization,"job"

def formatstring(value1):
    lower_words = value1.lower()
    get_words = re.split(',| ', lower_words)
    return get_words


def single(value1, queryset, label):
    queryset_array = list()
    if label == "position_title":
        for i in value1:
            results = queryset.filter(position_title__icontains=i)
            if results:
                queryset_array.append(results)
        return queryset_array
    elif label == "city":
        for i in value1:
            results = queryset.filter(city__icontains=i)
            if results:
                queryset_array.append(results)
        return queryset_array
    elif label == "job_specialization":
        for i in value1:
            results = queryset.filter(job_specialization__icontains=i)
            if results:
                queryset_array.append(results)
        return queryset_array
    else:
        results = queryset.filter(category=value1)
        queryset_array.append(results)
    return queryset_array

def multiple(queryset, value2, label):
    queryset_array = list()
    if label == "city":
        for i in queryset:
            for j in value2:
                results = i.filter(city__icontains=j)
                if results:
                    queryset_array.append(results)
        return queryset_array
    elif label == "job_specialization":
        for i in queryset:
            for j in value2:
                results = i.filter(job_specialization__icontains=j)
                if results:
                    queryset_array.append(results)
        return queryset_array

def apply_job(request,id):
    job = JobAd.objects.get(id=id)
    user = request.user.id 
    if request.method =='POST':
        obj = AppliedJob.objects.create(user_id=request.user.id,
                                        jobad_id=id
                                        )
        return redirect('searchjob:job_app')
    else:
        return redirect('searchjob:search')

def apply_free(request,id):
    job = Freelance.objects.get(id=id)
    user = request.user.id 
    if request.method =='POST':
        obj = AppliedFree.objects.create(user_id=request.user.id,
                                        freelance_id=id
                                        )
        return redirect('searchjob:free_app')
    else:
        return redirect('searchjob:freesearch')

def job_app(request):
    jobapplied = AppliedJob.objects.filter(user_id=request.user.id).select_related('jobad').order_by('-timestamp')
    return render(request, 'searchjob/job_app.html',{'jobapplied':jobapplied})

def free_app(request):
    jobapplied = AppliedFree.objects.filter(user_id=request.user.id).select_related('freelance').order_by('-timestamp')
    return render(request, 'searchjob/free_app.html',{'jobapplied':jobapplied})

def view_job(request,id):
    user = request.user.id
    jobview = JobAd.objects.get(id=id)
    if request.method =='POST':
        if ViewedJob.objects.filter(user_id=request.user.id).exists():
            viewjob=ViewedJob.objects.filter(user_id=request.user.id)
            if viewjob.filter(jobad_id=id).exists():
                return render(request, 'searchjob/view_job.html', {'jobview': jobview})
            else:
                viewed = ViewedJob.objects.create(user_id=request.user.id,
                                            jobad_id=id)
                return render(request, 'searchjob/view_job.html', {'jobview': jobview,'viewed':viewed})
        else:
            viewed = ViewedJob.objects.create(user_id=request.user.id,
                                            jobad_id=id)
            return render(request,'searchjob/view_job.html',{'jobview':jobview})
    else:
        return render(request, 'searchjob/view_job.html', {'jobview': jobview})

def freeview_job(request,id):
    user = request.user.id
    jobview = Freelance.objects.get(id=id)
    if request.method =='POST':
        if ViewedFree.objects.filter(user_id=request.user.id).exists():
            viewjob=ViewedFree.objects.filter(user_id=request.user.id)
            if viewjob.filter(freelance_id=id).exists():
                return render(request, 'searchjob/view_free.html', {'jobview': jobview})
            else:
                viewed = ViewedFree.objects.create(user_id=request.user.id,
                                            freelance_id=id)
                return render(request, 'searchjob/view_free.html', {'jobview': jobview,'viewed':viewed})
        else:
            viewed = ViewedFree.objects.create(user_id=request.user.id,
                                            freelance_id=id)
            return render(request,'searchjob/view_free.html',{'jobview':jobview})
    else:
        return render(request, 'searchjob/view_free.html', {'jobview': jobview})

def service_req(request):
    req = ServiceRequest.objects.filter(user_id=request.user.id).order_by('-timestamp')
    return render(request, 'searchjob/service_req.html',{'req':req})
