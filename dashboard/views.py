import re
import string
import plotly
import pgeocode
import operator
from functools import reduce
from django.apps import apps
from datetime import datetime
import plotly.graph_objs as go
from plotly.offline import plot
from collections import Counter
import plotly.figure_factory as ff
from django.shortcuts import render
from django.db.models import Count, Sum, Q
from django.contrib.auth.decorators import login_required


# @login_required(login_url='/employers/login/')
def dashboard(request):
    group = str(request.user.groups.get())
    if group == "Employers":
        if len(salary(request)) > 0:
            jobfilter = jobpostsfilter(request)
            queryset_1 = jobposts(request)
            queryset_2 = mostattractive(request)
            queryset_3 = application(request)
            queryset_4 = location(request)
            queryset_5a = salary(request)[0]
            queryset_5b = salary(request)[1]
            queryset_5c = salary(request)[2]
            queryset_6 = demoexperience(request)
            queryset_7 = demoeducation(request)
            return render(request, 'dashboard/tdashboard.html', {'group': group, 'jobfilter': jobfilter, 'queryset_1': queryset_1, 'queryset_2': queryset_2, 'queryset_3': queryset_3, 'queryset_4': queryset_4, 'queryset_5a': queryset_5a, 'queryset_5b': queryset_5b, 'queryset_5c': queryset_5c, 'queryset_6': queryset_6, 'queryset_7': queryset_7})
        else:
            queryset_1 = jobposts(request)
            queryset_2 = mostattractive(request)
            queryset_3 = application(request)
            queryset_4 = location(request)
            queryset_5 = salary(request)
            return render(request, 'dashboard/tdashboard.html', {'group': group, 'queryset_1': queryset_1, 'queryset_2': queryset_2, 'queryset_3': queryset_3, 'queryset_4': queryset_4, 'queryset_5': queryset_5})
    else:
        queryset_1 = [upcoming(request), completed(
            request), nextservice(request)]
        queryset_2 = bookhistory(request)
        queryset_2.sort(key=lambda x: -x[1])
        queryset_3 = mostsearched(request)
        queryset_4 = nearyou(request)
        queryset_4.sort(key=lambda x: x[1])
        queryset_5 = topproviders()
        return render(request, 'dashboard/sdashboard.html', {'group': group, 'queryset_1': queryset_1, 'queryset_2': queryset_2, 'queryset_3': queryset_3, 'queryset_4': queryset_4, 'queryset_5': queryset_5})


def jobpostsfilter(request):
    results = list()
    JobAd = apps.get_model('jobads', 'JobAd')
    jobad = JobAd.objects.filter(user_id=request.user.id)
    if jobad:
        now = datetime.now().date()
        for i in jobad:
            duration = (i.closing_date - now).days
            results.append([i.position_title, duration])
        results.sort(key=lambda x: (x[1] < 0, abs(x[1])))
        return results
    else:
        return []


def jobposts(request):
    ongoing = list()
    expired = list()
    JobAd = apps.get_model('jobads', 'JobAd')
    jobad = JobAd.objects.filter(
        user_id=request.user.id).order_by("closing_date")
    for i in jobad:
        now = datetime.now().date()
        duration = (i.closing_date - now).days
        if duration < 0:
            expired.append(i)
        else:
            ongoing.append(i)
    return len(ongoing), len(expired)


def mostattractive(request):
    JobAd = apps.get_model('jobads', 'jobad')
    Application = apps.get_model('jobads', 'unprocessed')
    total = Application.objects.filter(
        user_id=request.user.id).values('jobad_id').annotate(id__count=Count('id'))
    if total:
        highest = max(total, key=lambda x: x['id__count'])
        temp = list(highest.values())
        get_jobad = JobAd.objects.get(id=temp[0])
        return [get_jobad, temp[1]]
    else:
        return []


def application(request):
    Unprocessed = apps.get_model('jobads', 'unprocessed')
    Shortlist = apps.get_model('jobads', 'shortlist')
    Interview = apps.get_model('jobads', 'interview')
    NotSuitable = apps.get_model('jobads', 'notsuitable')
    unprocessed = Unprocessed.objects.filter(
        user_id=request.user.id).filter(status__isnull=True)
    shortlist = Shortlist.objects.filter(user_id=request.user.id)
    interview = Interview.objects.filter(user_id=request.user.id)
    notsuitable = NotSuitable.objects.filter(user_id=request.user.id)
    results = [["Total", unprocessed.count()], ["Shortlist", shortlist.count(
    )], ["Interview", interview.count()], ["Not Suitable", notsuitable.count()]]
    return results


def location(request):
    temp = list()
    results = list()
    Application = apps.get_model('jobads', 'unprocessed')
    Candidate = apps.get_model('test_cand', 'TestCand')
    application = Application.objects.filter(user_id=request.user.id)
    for i in application:
        location = Candidate.objects.filter(
            id=i.id).values('preferred_location')
        temp.extend(list(location[0].values())[0].split(", "))
    count = dict(Counter(temp))
    for i in zip(list(count.keys()), list(count.values())):
        results.append(list(i))
    return plotmap(getcoordinates(results))


def getcoordinates(results):
    latitude = list()
    longitude = list()
    doc = open("MY_coordinates.csv").read()
    temp = ''.join(i for i in doc if not i.isdigit())
    state = ''.join(
        i for i in temp if i not in string.punctuation).rsplit("\n")
    coordinates = re.findall(r'\d+\.\d+', doc)
    for key, value in enumerate(coordinates):
        if key % 2 == 0:
            latitude.append(value)
        else:
            longitude.append(value)
    return comparestates(results, state, latitude, longitude)


def comparestates(queryset, state, latitude, longitude):
    temp = list()
    results = list()
    for i in zip(latitude, longitude):
        temp.append(list(i))
    for i in zip(state, temp):
        results.append(list(i))
    for i in queryset:
        for j in results:
            if i[0] == j[0]:
                i.append(j[1])
                i.pop(0)
    return queryset


def separatedata(data):
    size = list()
    latitude = list()
    longitude = list()
    for i in data:
        size.append(i[0])
        latitude.append(float(i[1][0]))
        longitude.append(float(i[1][1]))
    return size, latitude, longitude


def plotmap(data):
    results = separatedata(data)
    mapbox_access_token = open(
        "/Users/phooi/projects/jobpillar/mapbox_token.txt").read()
        # "/Users/janessalee/Sites/fyp/JobPillar/mapbox_token.txt").read()
    scatter = go.Figure(go.Scattermapbox(lat=results[1], lon=results[2], mode='markers', text=results[0],
                                         hovertemplate='Total: %{text}<extra></extra>',
                                         marker={'size': 4, 'color': '#003776'}),
                        go.Layout(mapbox_style="carto-positron", hovermode='closest', width=376, height=230,
                                  mapbox={'accesstoken': mapbox_access_token, 'pitch': 0, 'bearing': 0,
                                          'center': {'lat': 3.974341, 'lon': 108.78068}, 'zoom': 3.6},
                                  margin={'t': 0, 'r': 0, 'l': 0, 'b': 0}, hoverlabel={'font_family': 'Poppins', 'bgcolor': 'white'}))
    plot_div = plot(scatter, include_plotlyjs=False,
                    output_type='div', config={'displayModeBar': False})
    return plot_div


def salary(request):
    results = list()
    Application = apps.get_model('jobads', 'unprocessed')
    Candidate = apps.get_model('test_cand', 'TestCand')
    application = Application.objects.filter(user_id=request.user.id)
    for i in application:
        candidate = Candidate.objects.get(id=i.cand_id)
        results.append(candidate.expected_salary)
    if results:
        results.sort()
        count = dict(Counter(results))
        data = list(count.keys())
        lowest = min(data)
        highest = max(data)
        average = sum(data)/len(data)
        return int(average), len(data), plothist(data, lowest, average, highest)
    else:
        return []


def plothist(data, lowest, average, highest):
    plot_div = plot({
        "data": [go.Histogram(x=data, nbinsx=10, marker={'color': '#e1f0ff'}, histnorm='probability density',
                              hovertemplate='RM %{x}<extra></extra>')],
        "layout": go.Layout(width=300, height=210, margin=go.layout.Margin(l=0, r=0, b=0, t=20),
                            plot_bgcolor='white', font={'family': 'Poppins', 'color': '#999999'},
                            yaxis={'fixedrange': True, 'visible': False},
                            xaxis={'showgrid': False, 'fixedrange': True,
                                   'tickvals': [lowest, int(average), highest],
                                   'ticktext': ["RM " + str(lowest) + "<br>Low", "RM " + str(int(average)) + "<br>Average", "RM " + str(highest) + "<br>High"]},
                            hoverlabel={'font_family': 'Poppins',
                                        'bgcolor': 'white'},
                            bargroupgap=0.1)},
        output_type="div", config={'displayModeBar': False})
    return plot_div


def demoexperience(request):
    temp = list()
    years = list()
    group1 = list()
    group2 = list()
    group3 = list()
    group4 = list()
    Application = apps.get_model('jobads', 'unprocessed')
    Experience = apps.get_model('test_cand', 'CandExp')
    application = Application.objects.filter(user_id=request.user.id)
    for i in application:
        experience = Experience.objects.filter(cand_id=i.id).values(
            'cand_id').annotate(Count('cand_id'))
        temp.extend(experience)
    for i in temp:
        if list(i.values())[1] == 0:
            group1.append(list(i.values())[1])
        elif list(i.values())[1] < 4 and list(i.values())[1] > 0:
            group2.append(list(i.values())[1])
        elif list(i.values())[1] < 7 and list(i.values())[1] > 3:
            group3.append(list(i.values())[1])
        else:
            group4.append(list(i.values())[1])
    results = [["0", len(group1)], ["1-3", len(group2)],
               ["4-6", len(group3)], ["> 6", len(group4)]]
    for key, value in enumerate(results):
        if value[1] == 0:
            results.pop(key)
    return plotdonut(results)


def plotdonut(results):
    labels = list()
    values = list()
    for i in results:
        labels.append(i[0])
        values.append(i[1])
    plot_div = plot({
        "data": [go.Pie(labels=labels, values=values, hole=0.7, textposition='outside', hoverinfo='none')],
        "layout": go.Layout(width=360, height=200, margin=go.layout.Margin(l=0, r=0, b=0, t=28),
                            plot_bgcolor='white', font={'family': 'Poppins', 'color': '#999999'},
                            hoverlabel={'font_family': 'Poppins',
                                        'bgcolor': 'white'},
                            legend={'orientation': 'h', 'xanchor': 'left', 'x': 0, 'itemclick': False,
                                    'yanchor': 'top', 'y': -0.15, 'itemdoubleclick': False},
                            colorway=['#002e6b', '#66aacc', '#d8eaf2', '#ebf4f8'])},
        output_type="div", config={'displayModeBar': False})
    return plot_div


def demoeducation(request):
    temp = list()
    Application = apps.get_model('jobads', 'unprocessed')
    Education = apps.get_model('test_cand', 'CandEdu')
    application = Application.objects.filter(user_id=request.user.id)
    for i in application:
        education = Education.objects.filter(cand_id=i.id).filter(reduce(operator.or_, (Q(
            title__icontains=i) for i in ['certificate', 'doctorate', 'bachelor', "bachelor's", 'diploma', 'master', "master's", 'secondary'])))
        temp.extend(education)
    diploma = extractstring(temp, 'diploma')
    bachelor = extractstring(temp, 'bachelor')
    master = extractstring(temp, 'master')
    doctorate = extractstring(temp, 'doctorate')
    others = len(temp) - (len(diploma) + len(bachelor) +
                          len(master) + len(doctorate))
    results = [["Diploma", len(diploma)], ["Bachelor", len(bachelor)],
               ["Master", len(master)], ["Doctorate", len(doctorate)], ["Others", others]]
    for key, value in enumerate(results):
        if value[1] == 0:
            results.pop(key)
    return plotbar1(results)


def extractstring(temp, text):
    diploma = list()
    bachelor = list()
    master = list()
    doctorate = list()
    if text == "diploma":
        for i in temp:
            results = re.findall(text, i.title, flags=re.IGNORECASE)
            if results:
                diploma.extend(results)
        return diploma
    elif text == "bachelor":
        for i in temp:
            results = re.findall(text, i.title, flags=re.IGNORECASE)
            if results:
                bachelor.extend(results)
        return bachelor
    elif text == "master":
        for i in temp:
            results = re.findall(text, i.title, flags=re.IGNORECASE)
            if results:
                master.extend(results)
        return master
    else:
        for i in temp:
            results = re.findall(text, i.title, flags=re.IGNORECASE)
            if results:
                doctorate.extend(results)
        return doctorate


def plotbar1(results):
    labels = list()
    values = list()
    for i in results:
        labels.append(i[0])
        values.append(i[1])
    plot_div = plot({
        "data": [go.Bar(x=values, y=labels, orientation='h', width=0.62, marker={'color': values, 'colorscale': 'blues'},
                        hovertemplate='Total: %{x}<extra></extra>')],
        "layout": go.Layout(width=300, height=200, margin=go.layout.Margin(l=0, r=0, b=0, t=20, pad=8),
                            plot_bgcolor='white', font={'family': 'Poppins', 'color': '#999999'},
                            yaxis={'categoryorder': 'total ascending',
                                   'fixedrange': True},
                            xaxis={'showgrid': False,
                                   'visible': False, 'fixedrange': True},
                            hoverlabel={'font_family': 'Poppins',
                                        'bgcolor': 'white'})},
        output_type="div", config={'displayModeBar': False})
    return plot_div


def upcoming(request):
    Booking = apps.get_model('booking', 'Booking')
    booking = Booking.objects.filter(
        user_id=request.user.id).order_by("booked_date")
    completed = Booking.objects.filter(
        user_id=request.user.id).filter(job_status="Complete")
    cancelled = Booking.objects.filter(
        user_id=request.user.id).filter(job_status="Cancelled")
    results = booking.count() - completed.count() - cancelled.count()
    return results


def completed(request):
    Booking = apps.get_model('booking', 'Booking')
    completed = Booking.objects.filter(
        user_id=request.user.id).filter(job_status="Complete").filter(hidden__isnull=True)
    results = completed.count()
    return results


def nextservice(request):
    queryset_array = list()
    now = datetime.now().date()
    Booking = apps.get_model('booking', 'Booking')
    Service = apps.get_model('service', 'Service')
    details = Service.objects.filter(booking__in=Booking.objects.filter(user_id=request.user.id).filter(
        job_status__isnull=True).filter(booked_date__gt=now)).order_by("booking__booked_date")
    booking = Booking.objects.filter(user_id=request.user.id).filter(
        job_status__isnull=True).filter(booked_date__gt=now).order_by("booked_date")
    if details and booking:
        duration = caldays(booking)
        for i in zip(booking, details):
            queryset_array.append(i)
        return queryset_array, duration
    else:
        return []


def caldays(booking):
    now = datetime.now().date()
    temp = booking[0].booked_date - now
    return temp.days


def bookhistory(request):
    queryset_array = list()
    Booking = apps.get_model('booking', 'Booking')
    Service = apps.get_model('service', 'Service')
    total = Booking.objects.filter(
        user_id=request.user.id).values('service_id').annotate(Count('id')).filter(id__count__gt=1)
    for i in total:
        temp = list(i.values())
        booking = Booking.objects.filter(
            user_id=request.user.id).filter(service_id=temp[0])
        details = Service.objects.filter(
            booking__in=Booking.objects.filter(user_id=request.user.id)).filter(id=temp[0])
        if len(booking) and len(details) > 1:
            queryset_array.append([details[0], temp[1]])
    return queryset_array


def categorise(results):
    results.sort(key=lambda x: -x[1])
    x_data = list()
    y_data = list()
    for i in results:
        x_data.append(i[1])
        y_data.append(i[0])
    return x_data, y_data


def mostsearched(request):
    results = list()
    Search = apps.get_model('search', 'SSearch')
    total = Search.objects.filter(user_id=request.user.id).values(
        'service_type').annotate(Count('id')).filter(id__count__gt=0)
    for i in total:
        temp = list(i.values())
        if temp[1] < 2:
            search = Search.objects.filter(
                user_id=request.user.id).filter(service_type=temp[0])
            for i in search:
                results.append([i.service_type, int(i.total_search)])
        else:
            search = Search.objects.filter(
                user_id=request.user.id).filter(service_type=temp[0]).values('service_type').annotate(Sum('total_search'))
            for i in search:
                convert = list(i.values())
                results.append(convert)
    if results:
        return plotbar2(categorise(results))
    else:
        return []


def plotbar2(data):
    plot_div = plot({
        "data": [go.Bar(x=data[0][:7], y=data[1][:7], orientation='h', width=0.62, marker={'color': data[0], 'colorscale': 'blues'},
                        hovertemplate='Total: %{x}<extra></extra>')],
        "layout": go.Layout(width=368, height=230, margin=go.layout.Margin(l=0, r=0, b=0, t=0, pad=8),
                            plot_bgcolor='white', font={'family': 'Poppins', 'color': '#999999'},
                            yaxis={'categoryorder': 'total ascending',
                                   'fixedrange': True},
                            xaxis={'showgrid': False,
                                   'visible': False, 'fixedrange': True},
                            hoverlabel={'font_family': 'Poppins',
                                        'bgcolor': 'white'})},
        output_type="div", config={'displayModeBar': False})
    return plot_div


def nearyou(request):
    results = list()
    Service = apps.get_model('service', 'Service')
    Individual = apps.get_model('employers', 'Individual')
    individual = Individual.objects.get(user_id=request.user.id)
    dist = pgeocode.GeoDistance('MY')
    for i in Service.objects.all():
        distance = dist.query_postal_code(i.pcode, individual.pcode)
        results.append([i, distance])
    results.sort(key=lambda x: x[1])
    return results


def topproviders():
    Service = apps.get_model('service', 'Service')
    results = Service.objects.filter(rating=5).order_by("-jobs_completed")
    return results
