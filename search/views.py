import re
import ssl
import plotly
import operator
import pgeocode
import collections
from functools import reduce
from django.apps import apps
from plotly.offline import plot
import plotly.graph_objects as go
from django.contrib import messages
from .models import SSearch, Message
from django.db.models import Q, Func
from django.shortcuts import render, redirect
from django.db.models.functions import StrIndex
from django.contrib.auth.decorators import login_required


# @login_required(login_url='/employers/login/')
def search(request):
    group = str(request.user.groups.get())
    if group == "Employers":
        results = tsearch(request)
        if results:
            if len(results) == 2:
                queryset_array = results[0]
                position_title = results[1]
                return render(request, 'search/tsearch.html', {'queryset_array': queryset_array, 'position_title': position_title})
            elif len(results) == 4:
                queryset_array = results[0]
                position_title = results[1]
                keywords = results[2]
                skills = results[3]
                return render(request, 'search/tsearch.html', {'queryset_array': queryset_array, 'position_title': position_title, 'keywords': keywords, 'skills': skills})
            else:
                queryset_array = results[0]
                position_title = results[1]
                if results[3] == "keywords":
                    keywords = results[2]
                    return render(request, 'search/tsearch.html', {'queryset_array': queryset_array, 'position_title': position_title, 'keywords': keywords})
                else:
                    skills = results[2]
                    return render(request, 'search/tsearch.html', {'queryset_array': queryset_array, 'position_title': position_title, 'skills': skills})
        else:
            return render(request, 'search/tsearch.html')
    else:
        queryset_array = list()
        results = ssearch(request)
        if results:
            if results[2][0] and results[2][1]:
                scattermapbox = plotmap(
                    results[2][0], results[2][1], results[0])
                queryset_array = results[0]
                queryset_array.sort(key=lambda x: x[1])
                location = results[1]
                return render(request, 'search/ssearch.html', {'queryset_array': queryset_array, 'location': location, 'scattermapbox': scattermapbox})
            else:
                queryset_array = results[0]
                queryset_array.sort(key=lambda x: x[1])
                location = results[1]
                return render(request, 'search/ssearch.html', {'queryset_array': queryset_array, 'location': location})
        else:
            return render(request, 'search/ssearch.html')


def formatstring(value):
    lower_words = value.lower()
    get_words = re.compile("\w+").findall(lower_words)
    return get_words


def tsearch(request):
    queryset_array = list()
    TestCand = apps.get_model('test_cand', 'TestCand')
    position_title = request.GET.get('position_title')
    keywords = request.GET.get('keywords')
    skills = request.GET.get('skills')
    if position_title:
        results1 = TestCand.objects.filter(reduce(operator.or_, (Q(
            title__icontains=i) for i in formatstring(position_title))))
        if keywords:
            results2 = results1.filter(reduce(operator.or_, (Q(
                description__icontains=i) for i in formatstring(keywords))))
            if skills:
                results3 = results2.filter(reduce(operator.or_, (Q(
                    skills__icontains=i) for i in formatstring(skills))))
                queryset_array.append(getcand(results3))
                return queryset_array, position_title, keywords, skills
            else:
                queryset_array.append(getcand(results2))
                return queryset_array, position_title, keywords, "keywords", ""
        elif skills:
            results2 = results1.filter(reduce(operator.or_, (Q(
                skills__icontains=i) for i in formatstring(skills))))
            queryset_array.append(getcand(results2))
            return queryset_array, position_title, skills, "skills", ""
        else:
            queryset_array.append(sortquery(results1, position_title))
            return queryset_array, position_title


def sortquery(queryset, value):
    temp = list()
    results = list()
    for i in queryset:
        temp.append([i.title.lower().find(value), len(i.title), i])
    temp.sort(key=lambda x: (x[0] < 0, x[0], x[1]))
    for i in temp:
        i.pop(0)
        i.pop(0)
        results.extend(i)
    return getcand(results)


def getcand(queryset):
    results = list()
    CandEdu = apps.get_model('test_cand', 'CandEdu')
    CandExp = apps.get_model('test_cand', 'CandExp')
    for i in queryset:
        education = CandEdu.objects.filter(cand_id=i.id).first()
        experience = CandExp.objects.filter(cand_id=i.id).count()
        results.append([i, education, experience])
    return results


def candidate(request, id):
    temp = list()
    Profile = apps.get_model('test_cand', 'TestCand')
    Education = apps.get_model('test_cand', 'CandEdu')
    Experience = apps.get_model('test_cand', 'CandExp')
    details = Profile.objects.get(id=id)
    formatskills = details.skills.split(',')
    for i in formatskills:
        temp.append([len(i), i])
    temp.sort(key=lambda x: x[0])
    education = Education.objects.filter(cand_id=id)
    experience = Experience.objects.filter(cand_id=id)
    return render(request, 'search/candidate.html', {'details': details, 'formatskills': temp, 'education': education, 'experience': experience})


def contact(request, id):
    TestCand = apps.get_model('test_cand', 'TestCand')
    candidate = TestCand.objects.get(id=id)
    if request.method == 'POST':
        obj = Message.objects.create(
            user_id=request.user.id, cand_id=id, messages=request.POST['message'])
        messages.success(request, "Your message has been sent!")
        return redirect('jobads:jobads')
    else:
        return render(request, 'search/message.html', {'candidate': candidate})


def ssearch(request):
    final_queryset_array = list()
    Service = apps.get_model('service', 'Service')
    Individual = apps.get_model('employers', 'Individual')
    individual = Individual.objects.get(user_id=request.user.id)
    category = request.POST.get('type')
    service_type = checkcategory(request, category)
    location = request.POST.get('location')
    if category:
        queryset_array = ss_single(category, Service)
        if service_type:
            queryset_array = ss_multiple(
                queryset_array, service_type, "service_type")
            if location:
                queryset_array = ss_multiple(
                    queryset_array, location, "location")
                distance = caldistance(queryset_array, individual)
                latandlon = getlatandlon(queryset_array)
                savesearch2(request, category, service_type, location)
                for i in zip(queryset_array, distance):
                    final_queryset_array.append(i)
            return final_queryset_array, location, latandlon


def checkcategory(request, category):
    if category == "Home":
        service_type = request.POST.get('home')
        return service_type
    elif category == "Office":
        service_type = request.POST.get('office')
        return service_type
    elif category == "Events":
        service_type = request.POST.get('events')
        return service_type
    elif category == "Lessons":
        service_type = request.POST.get('lessons')
        return service_type
    else:
        service_type = request.POST.get('health')
        return service_type


def ss_single(value1, Service):
    queryset_array = list()
    results = Service.objects.filter(category=value1)
    queryset_array.append(results)
    return queryset_array


def ss_multiple(queryset, value2, label):
    queryset_array = list()
    if label == "service_type":
        for i in queryset:
            results = i.filter(service_type=value2)
            queryset_array.append(results)
        return queryset_array
    else:
        for i in queryset:
            results = i.filter(state=value2).order_by(
                "jobs_completed")
        return results


def caldistance(queryset_array, individual):
    results = list()
    dist = pgeocode.GeoDistance('MY')
    for i in queryset_array:
        distance = dist.query_postal_code(i.pcode, individual.pcode)
        results.append(distance)
    return results


def savesearch2(request, category, service_type, location):
    obj = SSearch.objects.filter(category=category).filter(
        service_type=service_type).filter(location=location).exists()
    if obj is False:
        SSearch.objects.create(
            user_id=request.user.id,
            category=category,
            service_type=service_type,
            location=location,
            total_search=1)
    else:
        obj = SSearch.objects.filter(category=category).filter(
            service_type=service_type).filter(location=location)
        for i in obj:
            i.total_search = int(i.total_search) + 1
            i.save()


def getlatandlon(queryset_array):
    latitude = list()
    longitude = list()
    nomi = pgeocode.Nominatim('MY')
    for i in queryset_array:
        latitude.append(nomi.query_postal_code(i.pcode).latitude)
        longitude.append(nomi.query_postal_code(i.pcode).longitude)
    return latitude, longitude


def plotmap(latitude, longitude, queryset_array):
    results = list()
    for i in queryset_array:
        temp = str(i[0].name) + " [" + str(round(i[1], 2)) + " km]"
        results.append(temp)
    mapbox_access_token = open(
        "/Users/janessalee/Sites/fyp/JobPillar/mapbox_token.txt").read()
    scatter = go.Figure(go.Scattermapbox(lat=latitude, lon=longitude, mode='markers', text=results,
                                         hoverinfo='text', marker={'size': 10, 'color': 'red'}),
                        go.Layout(mapbox_style="carto-positron", hovermode='closest', width=678, height=450,
                                  mapbox={'accesstoken': mapbox_access_token, 'pitch': 0, 'bearing': 0,
                                          'center': {'lat': latitude[0], 'lon': longitude[0]}, 'zoom': 9.5},
                                  margin={'t': 0, 'r': 0, 'l': 0, 'b': 0}, hoverlabel={'font_family': 'Poppins', 'bgcolor': 'white'}))
    results = plot(scatter, include_plotlyjs=False,
                   output_type='div', config={'displayModeBar': False})
    return results
