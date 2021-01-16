import re
import string
import plotly
import pandas as pd
from io import BytesIO
from django.apps import apps
import plotly.graph_objs as go
from plotly.offline import plot
from collections import Counter
from django.db.models import Count
from django.shortcuts import redirect, render
from reportlab.pdfgen import canvas
from django.http import FileResponse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('/admin/logout')


@staff_member_required
def dashboard(request):
    results = combineall(request)
    if results:
        queryset_1 = results[0]
        queryset_2 = results[1]
        queryset_3 = results[2]
        queryset_4 = results[3]
        queryset_5 = results[4]
        queryset_6 = results[5]
        queryset_7 = results[6]
        report = results[7]
        return render(request, 'customadmin/adashboard.html', {'queryset_1': queryset_1, 'queryset_2': queryset_2, 'queryset_3': queryset_3, 'queryset_4': queryset_4, 'queryset_5': queryset_5, 'queryset_6': queryset_6, 'queryset_7': queryset_7})
    else:
        return render(request, 'customadmin/adashboard.html')


def combineall(request):
    results1 = totalemployers()
    results2 = totalposts()
    results3 = servicetype()
    results4 = locofind()
    results5 = orgsize()
    results6 = industry()
    results7 = locofjob()
    results8 = generatereport(request)
    return results1, results2, results3, results4, results5, results6, results7, results8


def totalemployers():
    Organisation = apps.get_model('employers', 'Employer')
    Individual = apps.get_model('employers', 'Individual')
    organisation = Organisation.objects.all().count()
    individual = Individual.objects.all().count()
    return organisation, individual


def totalposts():
    Jobad = apps.get_model('jobads', 'JobAd')
    Service = apps.get_model('service', 'Service')
    jobad = Jobad.objects.all().count()
    service = Service.objects.all().count()
    return jobad, service


def categorise(results):
    results.sort(key=lambda x: -x[1])
    x_data = list()
    y_data = list()
    for i in results:
        x_data.append(i[1])
        y_data.append(i[0])
    return x_data, y_data


def servicetype():
    results = list()
    Service = apps.get_model('service', 'Service')
    Booking = apps.get_model('booking', 'Booking')
    booking = Service.objects.filter(
        booking__in=Booking.objects.all()).values('service_type').annotate(Count('id'))
    for i in booking:
        results.append(list(i.values()))
    return plotbar1(categorise(results))


def plotbar1(data):
    plot_div = plot({
        "data": [go.Bar(x=data[0][:10], y=data[1][:10], orientation='h', width=0.62, marker={'color': data[0][:10], 'colorscale': 'blues'},
                        hovertemplate='Total: %{x}<extra></extra>')],
        "layout": go.Layout(width=366, height=315, margin=go.layout.Margin(l=0, r=0, b=0, t=0, pad=8),
                            plot_bgcolor='white', font={'family': 'Poppins', 'color': '#999999'},
                            yaxis={'categoryorder': 'total ascending',
                                   'fixedrange': True},
                            xaxis={'showgrid': False,
                                   'visible': False, 'fixedrange': True},
                            hoverlabel={'font_family': 'Poppins',
                                        'bgcolor': 'white'})},
        output_type="div", config={'displayModeBar': False})
    return plot_div


def formataddress(address):
    if address.count(', ') == 5:
        temp = address.rsplit(", ")[-1]
        return temp
    elif address.count(', ') == 4:
        temp = address.rsplit(", ")[-1]
        return temp
    else:
        temp = address.rsplit(", ")[-1]
        return temp


def locofind():
    temp = list()
    results = list()
    Individual = apps.get_model('employers', 'Individual')
    individual = Individual.objects.all()
    for i in individual:
        temp.append(replacestate(formataddress(i.address)))
    grouping = {i: temp.count(i) for i in temp}
    state = list(grouping.keys())
    total = list(grouping.values())
    for i in zip(state, total):
        results.append(list(i))
    return plotmap1(getcoordinates(results))


def plotmap1(data):
    results = separatedata(data)
    mapbox_access_token = open(
        "/Users/janessalee/Sites/fyp/JobPillar/mapbox_token.txt").read()
    scatter = go.Figure(go.Scattermapbox(lat=results[1], lon=results[2], mode='markers', text=results[0],
                                         hovertemplate='Total: %{text}<extra></extra>',
                                         marker={'color': '#003776', 'size': 4}),
                        go.Layout(mapbox_style="carto-positron", hovermode='closest', width=375, height=300,
                                  mapbox={'accesstoken': mapbox_access_token, 'pitch': 0, 'bearing': 0, 'zoom': 3.6,
                                          'center': {"lat": 3.2105, "lon": 109.2758}},
                                  margin={'t': 0, 'r': 0, 'l': 0, 'b': 0}, hoverlabel={'font_family': 'Poppins', 'bgcolor': 'white'}))
    plot_div = plot(scatter, include_plotlyjs=False,
                    output_type='div', config={'displayModeBar': False})
    return plot_div


def orgsize():
    small = list()
    medium = list()
    large = list()
    Organisation = apps.get_model('employers', 'Employer')
    organisation = Organisation.objects.all()
    for i in organisation:
        get_num = i.size.split(" ")
        if int(get_num[2]) <= 50:
            small.append(i)
        elif int(get_num[2]) <= 250:
            medium.append(i)
        else:
            large.append(i)
    return plotdonut(len(small), len(medium), len(large))


def plotdonut(small, medium, large):
    labels = ['Small', 'Medium', 'Large']
    values = [small, medium, large]
    plot_div = plot({
        "data": [go.Pie(labels=labels, values=values, hole=0.7, textposition='outside', hoverinfo='none')],
        "layout": go.Layout(width=400, height=290, margin=go.layout.Margin(l=0, r=0, b=0, t=30, pad=8),
                            plot_bgcolor='white', font={'family': 'Poppins', 'color': '#999999'},
                            hoverlabel={'font_family': 'Poppins',
                                        'bgcolor': 'white'},
                            legend={'orientation': 'h', 'yanchor': 'top', 'y': -0.15,
                                    'xanchor': 'left', 'x': 0.01, 'itemclick': False, 'itemdoubleclick': False},
                            colorway=['#002e6b', '#66aacc', '#d8eaf2'])},
        output_type="div", config={'displayModeBar': False})
    return plot_div


def industry():
    results = list()
    JobAd = apps.get_model('jobads', 'JobAd')
    total = JobAd.objects.values('job_specialization').annotate(
        Count('id')).filter(id__count__gt=0)
    for i in total:
        temp = list(i.values())
        results.append(temp)
    return plotbar2(categorise(results))


def plotbar2(data):
    plot_div = plot({
        "data": [go.Bar(x=data[0][:10], y=data[1][:10], orientation='h', width=0.62, marker={'color': data[0], 'colorscale': 'blues'},
                        hovertemplate='Total: %{x}<extra></extra>')],
        "layout": go.Layout(width=370, height=315, margin=go.layout.Margin(l=0, r=0, b=0, t=0, pad=8),
                            plot_bgcolor='white', font={'family': 'Poppins', 'color': '#999999'},
                            yaxis={'categoryorder': 'total ascending',
                                   'fixedrange': True},
                            xaxis={'showgrid': False,
                                   'visible': False, 'fixedrange': True},
                            hoverlabel={'font_family': 'Poppins',
                                        'bgcolor': 'white'})},
        output_type="div", config={'displayModeBar': False})
    return plot_div


def replacestate(address):
    if address == "Pulau Pinang":
        address = "Penang"
        return address
    elif address == "Selangor Darul Ehsan":
        address = "Selangor"
        return address
    elif address == "Putrajaya":
        address = "Selangor"
        return address
    elif address == "Labuan":
        address = "Sabah"
        return address
    elif address == "Kelantan Darul Naim":
        address = "Kelantan"
        return address
    else:
        return address


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


def locofjob():
    results = list()
    JobAd = apps.get_model('jobads', 'JobAd')
    jobad = JobAd.objects.values('location').annotate(Count('id'))
    for i in jobad:
        temp = list(i.values())
        results.append(temp)
    return plotmap2(getcoordinates(results))


def plotmap2(data):
    results = separatedata(data)
    mapbox_access_token = open(
        "/Users/janessalee/Sites/fyp/JobPillar/mapbox_token.txt").read()
    scatter = go.Figure(go.Scattermapbox(lat=results[1], lon=results[2], mode='markers', text=results[0],
                                         hovertemplate='Total: %{text}<extra></extra>',
                                         marker={'color': '#003776', 'size': 4}),
                        go.Layout(mapbox_style="carto-positron", hovermode='closest', width=375, height=300,
                                  mapbox={'accesstoken': mapbox_access_token, 'pitch': 0, 'bearing': 0, 'zoom': 3.6,
                                          'center': {"lat": 3.2105, "lon": 109.2758}},
                                  margin={'t': 0, 'r': 0, 'l': 0, 'b': 0}, hoverlabel={'font_family': 'Poppins', 'bgcolor': 'white'}))
    plot_div = plot(scatter, include_plotlyjs=False,
                    output_type='div', config={'displayModeBar': False})
    return plot_div


def generatereport(request):
    if request.method == 'POST':
        # buffer = io.BytesIO()
        # p = canvas.Canvas(buffer)
        # p.drawString(100, 100, "Hello world.")
        # p.showPage()
        # p.save()
        # buffer.seek(0)
        # return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="hello.pdf"'
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 100, 'Hello world.')
        p.showPage()
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        raise Exception(response)
        return response
    else:
        return render(request, 'customadmin/adashboard.html')


# import os
# from django.conf import settings
# from django.http import HttpResponse
# from django.template import Context
# from django.template.loader import get_template
# from xhtml2pdf import pisa


def generate_PDF(request):
    data = {}

    template = get_template('template_testing.html')
    html = template.render(Context(data))

    file = open('test.pdf', "w+b")
    pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
                                encoding='utf-8')

    file.seek(0)
    pdf = file.read()
    file.close()
    return HttpResponse(pdf, 'application/pdf')
