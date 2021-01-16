import re
import sqlite3
import pandas as pd
from django.apps import apps
from datetime import datetime
from django.core import serializers
from django.contrib import messages
from django.http import JsonResponse
from .forms import JobAdForm, InvitationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import JobAd, Shortlist, Interview, Unprocessed, NotSuitable, Invitation, joblist

job_match_list = []
sme = [0, 0, 1, 1, -1]  # software management engineer
re = [-1, 1, 0, 1, -1]  # requirement engineer
sd = [-1, 1, 1, 1, -1]  # system designer
programmer = [-1, 0, 1, 1, -1]
tester = [1, 0, 0, 1, -1]
evaluator = [0, 1, 1, 1, -1]

job_match_list.append(sme)
job_match_list.append(re)
job_match_list.append(sd)
job_match_list.append(programmer)
job_match_list.append(tester)
job_match_list.append(evaluator)
# @login_required(login_url='/employers/login/')
def jobads(request):
    jobads = JobAd.objects.values().filter(user_id=request.user.id)
    job_list = joblist.objects.values()
    now = datetime.now().date()
    if not jobads:
        return render(request, 'jobads/jobads.html')
    return render(request, 'jobads/jobads.html', {'jobads': jobads, 'now': now, 'joblist':job_list})


def createjob(request):
    form = JobAdForm()
    if request.method == 'POST':
        convert_date = datetime.strptime(
            request.POST['closing_date'], '%m/%d/%Y')
        obj = JobAd.objects.create(
            user_id=request.user.id,
            position_title=request.POST['position_title'],
            employment_type=request.POST['employment_type'],
            position_level=request.POST['position_level'],
            job_specialization=request.POST['job_specialization'],
            job_description=request.POST['job_description'],
            job_requirements=request.POST['job_requirements'],
            location=request.POST['location'],
            min_salary=request.POST['min_salary'],
            max_salary=request.POST['max_salary'],
            closing_date=convert_date)
        messages.success(request, "A new job has been added!")
        return redirect('jobads:jobads')
    return render(request, 'jobads/createjob.html', {'form': form})


def editjob(request, id):
    obj = JobAd.objects.get(id=id)
    obj.save()
    form = JobAdForm(instance=obj)
    if request.method == 'POST':
        form = JobAdForm(request.POST, instance=obj)
        if form.is_valid() and form.has_changed():
            form.save()
            messages.success(request, "Record was updated successfully!")
            return redirect('jobads:jobads')
        else:
            messages.error(request, "You did not make any changes.")
            return redirect('jobads:jobads')
    return render(request, 'jobads/editjob.html', {'form': form, 'obj': obj})


def deletejob(request, id):
    obj = JobAd.objects.filter(id=id)
    if request.method == 'POST':
        obj.delete()
    return JsonResponse(serializers.serialize('json', obj), safe=False)


def unprocessed(request, id):
    queryset_array = list()
    jobads = JobAd.objects.get(id=id)
    location_query = request.GET.getlist('location[]')
    experience_query = request.GET.get('experience')
    education_query = request.GET.getlist('education[]')
    queryset_array = beforefiltercand(list(beforefilterall(request, id)))
    get_count = getcount(request.user.id, jobads)
    if location_query:
        filtered = "True"
        queryset_array = ts_single(queryset_array, location_query, "location")
        if experience_query or education_query:
            if experience_query:
                filtered = "True"
                queryset_array = ts_multiple(
                    queryset_array, experience_query, "experience")
                if education_query:
                    filtered = "True"
                    queryset_array = ts_multiple(
                        queryset_array, education_query, "education")
                    return render(request, 'jobads/unprocessed.html', {'queryset_array': queryset_array, 'jobads': jobads, 'get_count': get_count, 'filtered': filtered})
                else:
                    return render(request, 'jobads/unprocessed.html', {'queryset_array': queryset_array, 'jobads': jobads, 'get_count': get_count, 'filtered': filtered})
            else:
                if education_query:
                    filtered = "True"
                    queryset_array = ts_multiple(
                        queryset_array, education_query, "education")
                    return render(request, 'jobads/unprocessed.html', {'queryset_array': queryset_array, 'jobads': jobads, 'get_count': get_count, 'filtered': filtered})
        else:
            return render(request, 'jobads/unprocessed.html', {'queryset_array': queryset_array, 'jobads': jobads, 'get_count': get_count, 'filtered': filtered})
    elif experience_query:
        filtered = "True"
        queryset_array = ts_single(
            queryset_array, experience_query, "experience")
        if education_query:
            filtered = "True"
            queryset_array = ts_multiple(
                queryset_array, education_query, "education")
            return render(request, 'jobads/unprocessed.html', {'queryset_array': queryset_array, 'jobads': jobads, 'get_count': get_count, 'filtered': filtered})
        else:
            return render(request, 'jobads/unprocessed.html', {'queryset_array': queryset_array, 'jobads': jobads, 'get_count': get_count, 'filtered': filtered})
    elif education_query:
        filtered = "True"
        queryset_array = ts_single(
            queryset_array, education_query, "education")
        return render(request, 'jobads/unprocessed.html', {'queryset_array': queryset_array, 'jobads': jobads, 'get_count': get_count, 'filtered': filtered})
    else:
        get_count = getcount(request.user.id, jobads)
        return render(request, 'jobads/unprocessed.html', {'queryset_array': queryset_array, 'jobads': jobads, 'get_count': get_count})


def beforefilterall(request, id):
    jobads = JobAd.objects.get(id=id)
    Application = apps.get_model('jobads', 'Unprocessed')
    results = Application.objects.filter(
        user_id=request.user.id).filter(jobad_id=jobads.id).filter(status__isnull=True)
    total = results.count()
    return results


def beforefiltercand(results):
    queryset_array = list()
    TestCand = apps.get_model('test_cand', 'TestCand')
    CandEdu = apps.get_model('test_cand', 'CandEdu')
    CandExp = apps.get_model('test_cand', 'CandExp')
    for i in results:
        candidate = TestCand.objects.filter(id=i.cand_id)
        education = CandEdu.objects.filter(cand_id=i.cand_id).first()
        experience = CandExp.objects.filter(cand_id=i.cand_id).count()
        queryset_array.append([candidate, education, experience])
    return queryset_array


def getcount(id, jobads):
    total = Unprocessed.objects.filter(
        user_id=id).filter(jobad_id=jobads.id).filter(status__isnull=True).count()
    shortlist = Shortlist.objects.filter(
        user_id=id).filter(jobad_id=jobads.id).filter(hidden__isnull=True).count()
    interview = Interview.objects.filter(
        user_id=id).filter(jobad_id=jobads.id).filter(hidden__isnull=True).count()
    notsuitable = NotSuitable.objects.filter(
        user_id=id).filter(jobad_id=jobads.id).filter(hidden__isnull=True).count()
    invited = Invitation.objects.filter(
        user_id=id).filter(jobad_id=jobads.id).count()
    return total, shortlist, interview, notsuitable, invited


def ts_single(queryset, user_input, label):
    results = list()
    if label == "location":
        for key, value in enumerate(queryset):
            for j in user_input:
                if j.lower() == value[0][0].location.lower():
                    results.append(value)
        return results
    elif label == "experience":
        for key, value in enumerate(queryset):
            for j in user_input:
                if value[2] == int(user_input):
                    results.append(value)
        return results
    else:
        for key, value in enumerate(queryset):
            for j in user_input:
                if value[1] != None:
                    if value[1].title.lower().find(j.lower()) != -1:
                        results.append(value)
        return results


def ts_multiple(queryset, user_input, label):
    results = list()
    if label == "experience":
        for key, value in enumerate(queryset):
            for j in user_input:
                if value[2] == int(user_input):
                    results.append(value)
        return results
    else:
        for key, value in enumerate(queryset):
            for j in user_input:
                if value[1] != None:
                    if value[1].title.lower().find(j.lower()) != -1:
                        results.append(value)
        return results


def candidate(request, job, cand):
    temp = list()
    Profile = apps.get_model('test_cand', 'TestCand')
    Education = apps.get_model('test_cand', 'CandEdu')
    Experience = apps.get_model('test_cand', 'CandExp')
    details = Profile.objects.get(id=cand)
    formatskills = details.skills.split(',')
    for i in formatskills:
        temp.append([len(i), i])
    temp.sort(key=lambda x: x[0])
    education = Education.objects.filter(cand_id=cand)
    experience = Experience.objects.filter(cand_id=cand)
    return render(request, 'jobads/candidate.html', {'details': details, 'formatskills': temp, 'education': education, 'experience': experience, 'jobads': job})


def addtolist(request, id, data, origin, model, label):
    if label == "shortlist":
        checking = model.objects.filter(user_id=request.user.id).filter(
            jobad_id=id).filter(cand_id=data).exists()
        if checking is False:
            obj = model.objects.create(
                user_id=request.user.id,
                jobad_id=id,
                cand_id=data)
        if origin == "interview":
            obj = Interview.objects.get(cand_id=data)
            obj.hidden = "True"
            obj.save()
            if checking is True:
                obj = model.objects.get(cand_id=data)
                obj.hidden = None
                obj.save()
        if origin == "notsuitable":
            obj = NotSuitable.objects.get(cand_id=data)
            obj.hidden = "True"
            obj.save()
            if checking is True:
                obj = model.objects.get(cand_id=data)
                obj.hidden = None
                obj.save()
    elif label == "interview":
        checking = model.objects.filter(user_id=request.user.id).filter(
            jobad_id=id).filter(cand_id=data).exists()
        if checking is False:
            obj = model.objects.create(
                user_id=request.user.id,
                jobad_id=id,
                cand_id=data)
        if origin == "shortlist":
            obj = Shortlist.objects.get(cand_id=data)
            obj.hidden = "True"
            obj.save()
            if checking is True:
                obj = model.objects.get(cand_id=data)
                obj.hidden = None
                obj.save()
        if origin == "notsuitable":
            obj = NotSuitable.objects.get(cand_id=data)
            obj.hidden = "True"
            obj.save()
            if checking is True:
                obj = model.objects.get(cand_id=data)
                obj.hidden = None
                obj.save()
    else:
        checking = model.objects.filter(user_id=request.user.id).filter(
            jobad_id=id).filter(cand_id=data).exists()
        if checking is False:
            obj = model.objects.create(
                user_id=request.user.id,
                jobad_id=id,
                cand_id=data)
        if origin == "shortlist":
            obj = Shortlist.objects.get(cand_id=data)
            obj.hidden = "True"
            obj.save()
            if checking is True:
                obj = model.objects.get(cand_id=data)
                obj.hidden = None
                obj.save()
        if origin == "interview":
            obj = Interview.objects.get(cand_id=data)
            obj.hidden = "True"
            obj.save()
            if checking is True:
                obj = model.objects.get(cand_id=data)
                obj.hidden = None
                obj.save()


def updatelist(request, id, data):
    obj = Unprocessed.objects.filter(user_id=request.user.id).filter(
        jobad_id=id).filter(cand_id=data)
    for i in obj:
        i.status = "Processed"
        i.save()


def canddetails(id, model, label):
    results = list()
    Candidate = apps.get_model('test_cand', 'TestCand')
    Education = apps.get_model('test_cand', 'CandEdu')
    Experience = apps.get_model('test_cand', 'CandExp')
    if label == "shortlist":
        candidate = Candidate.objects.filter(
            id__in=model.objects.filter(jobad_id=id).filter(hidden__isnull=True).values('cand_id'))
        for i in candidate:
            education = Education.objects.filter(
                cand__in=Candidate.objects.filter(id=i.id)).first()
            experience = Experience.objects.filter(
                cand__in=Candidate.objects.filter(id=i.id)).count()
            results.append([i, education, experience])
        return results
    elif label == "interview":
        candidate = Candidate.objects.filter(
            id__in=model.objects.filter(jobad_id=id).filter(hidden__isnull=True).values('cand_id'))
        for i in candidate:
            education = Education.objects.filter(
                cand__in=Candidate.objects.filter(id=i.id)).first()
            experience = Experience.objects.filter(
                cand__in=Candidate.objects.filter(id=i.id)).count()
            results.append([i, education, experience])
        return results
    elif label == "notsuitable":
        candidate = Candidate.objects.filter(
            id__in=model.objects.filter(jobad_id=id).filter(hidden__isnull=True).values('cand_id'))
        for i in candidate:
            education = Education.objects.filter(
                cand__in=Candidate.objects.filter(id=i.id)).first()
            experience = Experience.objects.filter(
                cand__in=Candidate.objects.filter(id=i.id)).count()
            results.append([i, education, experience])
        return results
    else:
        candidate = Candidate.objects.filter(
            id__in=model.objects.filter(jobad_id=id).values('cand_id'))
        for i in candidate:
            education = Education.objects.filter(
                cand__in=Candidate.objects.filter(id=i.id)).first()
            experience = Experience.objects.filter(
                cand__in=Candidate.objects.filter(id=i.id)).count()
            results.append([i, education, experience])
        return results


def shortlist(request, id):
    jobads = JobAd.objects.get(id=id)
    get_count = getcount(request.user.id, jobads)
    Shortlist = apps.get_model('jobads', 'Shortlist')
    if request.method == 'POST':
        if "/" not in list(request.POST.keys())[1]:
            data = list(request.POST.keys())[1]
            addtolist(request, id, data, "", Shortlist, "shortlist")
            updatelist(request, id, data)
            get_count = getcount(request.user.id, jobads)
            get_candidate = list(canddetails(id, Shortlist, "shortlist"))
            return render(request, 'jobads/shortlist.html', {'jobads': jobads, 'get_count': get_count, 'get_candidate': get_candidate})
        else:
            data = list(request.POST.keys())[1].split("/")[0]
            origin = list(request.POST.keys())[1].split("/")[1]
            addtolist(request, id, data, origin, Shortlist, "shortlist")
            updatelist(request, id, data)
            get_count = getcount(request.user.id, jobads)
            get_candidate = list(canddetails(id, Shortlist, "shortlist"))
            return render(request, 'jobads/shortlist.html', {'jobads': jobads, 'get_count': get_count, 'get_candidate': get_candidate})
    else:
        if Shortlist.objects.count != 0:
            get_candidate = list(canddetails(id, Shortlist, "shortlist"))
            return render(request, 'jobads/shortlist.html', {'jobads': jobads, 'get_count': get_count, 'get_candidate': get_candidate})
        else:
            return render(request, 'jobads/shortlist.html', {'jobads': jobads, 'get_count': get_count})


def interview(request, id):
    jobads = JobAd.objects.get(id=id)
    get_count = getcount(request.user.id, jobads)
    Interview = apps.get_model('jobads', 'Interview')
    if request.method == 'POST':
        if "/" not in list(request.POST.keys())[1]:
            data = list(request.POST.keys())[1]
            addtolist(request, id, data, "", Interview, "interview")
            updatelist(request, id, data)
            get_count = getcount(request.user.id, jobads)
            get_candidate = list(canddetails(id, Interview, "interview"))
            return render(request, 'jobads/interview.html', {'jobads': jobads, 'get_count': get_count, 'get_candidate': get_candidate})
        else:
            data = list(request.POST.keys())[1].split("/")[0]
            origin = list(request.POST.keys())[1].split("/")[1]
            addtolist(request, id, data, origin, Interview, "interview")
            updatelist(request, id, data)
            get_count = getcount(request.user.id, jobads)
            get_candidate = list(canddetails(id, Interview, "interview"))
            return render(request, 'jobads/interview.html', {'jobads': jobads, 'get_count': get_count, 'get_candidate': get_candidate})
    else:
        if Interview.objects.count != 0:
            get_candidate = list(canddetails(id, Interview, "interview"))
            return render(request, 'jobads/interview.html', {'jobads': jobads, 'get_count': get_count, 'get_candidate': get_candidate})
        else:
            return render(request, 'jobads/interview.html', {'jobads': jobads, 'get_count': get_count})


def notsuitable(request, id):
    jobads = JobAd.objects.get(id=id)
    get_count = getcount(request.user.id, jobads)
    NotSuitable = apps.get_model('jobads', 'NotSuitable')
    if request.method == 'POST':
        if "/" not in list(request.POST.keys())[1]:
            data = list(request.POST.keys())[1]
            addtolist(request, id, data, "", NotSuitable, "notsuitable")
            updatelist(request, id, data)
            get_count = getcount(request.user.id, jobads)
            get_candidate = list(canddetails(id, NotSuitable, "notsuitable"))
            return render(request, 'jobads/notsuitable.html', {'jobads': jobads, 'get_count': get_count, 'get_candidate': get_candidate})
        else:
            data = list(request.POST.keys())[1].split("/")[0]
            origin = list(request.POST.keys())[1].split("/")[1]
            if origin == "delete":
                obj = NotSuitable.objects.filter(
                    jobad_id=id).filter(cand_id=data).delete()
                get_count = getcount(request.user.id, jobads)
                get_candidate = list(canddetails(
                    id, NotSuitable, "notsuitable"))
                return render(request, 'jobads/notsuitable.html', {'jobads': jobads, 'get_count': get_count, 'get_candidate': get_candidate})
            else:
                addtolist(request, id, data, origin,
                          NotSuitable, "notsuitable")
                updatelist(request, id, data)
                get_count = getcount(request.user.id, jobads)
                get_candidate = list(canddetails(
                    id, NotSuitable, "notsuitable"))
                return render(request, 'jobads/notsuitable.html', {'jobads': jobads, 'get_count': get_count, 'get_candidate': get_candidate})
    else:
        if NotSuitable.objects.count != 0:
            get_candidate = list(canddetails(id, NotSuitable, "notsuitable"))
            return render(request, 'jobads/notsuitable.html', {'jobads': jobads, 'get_count': get_count, 'get_candidate': get_candidate})
        else:
            return render(request, 'jobads/notsuitable.html', {'jobads': jobads, 'get_count': get_count})


def invitation(request, job, cand):
    TestCand = apps.get_model('test_cand', 'TestCand')
    candidate = TestCand.objects.get(id=cand)
    jobads = JobAd.objects.get(id=job)
    if request.method == 'POST':
        convert_date = datetime.strptime(
            request.POST['booked_date'], '%m/%d/%Y')
        checking = Invitation.objects.filter(user_id=request.user.id).filter(
            jobad_id=jobads.id).filter(cand_id=candidate.id).filter(
            booked_date=convert_date.date()).filter(booked_time=request.POST['booked_time']).filter(messages=request.POST['messages']).exists()
        if checking is False:
            temp = Interview.objects.filter(user_id=request.user.id).filter(
                jobad_id=jobads.id).filter(cand_id=candidate.id)
            for i in temp:
                i.hidden = "True"
                i.save()
            obj = Invitation.objects.create(
                user_id=request.user.id,
                jobad_id=jobads.id,
                cand_id=candidate.id,
                booked_date=convert_date.date(),
                booked_time=request.POST['booked_time'],
                messages=request.POST['messages'])
        return invited(request, job)
    else:
        form = InvitationForm()
        return render(request, 'jobads/invitation.html', {'form': form, 'candidate': candidate, 'jobads': jobads})


def invited(request, id):
    jobads = JobAd.objects.get(id=id)
    get_count = getcount(request.user.id, jobads)
    Invited = apps.get_model('jobads', 'Invitation')
    details = Invited.objects.filter(
        user_id=request.user.id).filter(jobad_id=id)
    if NotSuitable.objects.count != 0:
        get_candidate = list(canddetails(id, Invited, "invited"))
        for i in get_candidate:
            for j in details:
                if i[0].id == j.cand_id:
                    i.append(j.booked_date)
                    i.append(j.booked_time)
        get_candidate.sort(key=lambda x: (x[3], x[4]))
        return render(request, 'jobads/invited.html', {'jobads': jobads, 'get_count': get_count, 'get_candidate': get_candidate, 'details': details})
    else:
        return render(request, 'jobads/invited.html', {'jobads': jobads, 'get_count': get_count})


def view_ranking(request, id, jobid):
    jobads = JobAd.objects.get(id=id)
    job_list = joblist.objects.get(id=jobid)
    conn = sqlite3.connect('db.sqlite3')
    query = f"SELECT * FROM jobads_test_employee WHERE job_id_id='{jobid}' AND JobAd_id_id='{id}'"
    df = pd.read_sql_query(query, conn)

    df = df[['name', 'openess', 'conscientiousness',
                'extraversion', 'agreeableness', 'neuroticism']]
    dict = df.to_dict('index')
    result = {}
    for key in dict.keys():
        for x, y in dict[key].items():
            if x != 'name':
                y = int(y)
                if y <= 33:
                    result.setdefault(key, []).append([y, -1])
                elif y > 33 and y <= 67:
                    result.setdefault(key, []).append([y, 0])
                else:
                    result.setdefault(key, []).append([y, 1])

    score = []
    count = []
    print(result)
    for key in dict.keys():
        num = counter = 0
        for x in range(5):  
            if result[key][x][1] == job_match_list[int(jobid)-1][x]:
                df.iloc[key,x+1] = "✓"
                if result[key][x][1] == -1:
                    num -= result[key][x][0]
                    counter += 1
                else:
                    num += result[key][x][0]
                    counter += 1
            else:
                df.iloc[key,x+1] = "✗"
        score.append(num)
        count.append(counter)
    df['Match_count'] = count
    df['score'] = score
    df.sort_values(by=['Match_count', 'score'], ascending=False, inplace=True)

    df.drop(['score'], axis=1, inplace=True)

    df5 = df.loc[df['Match_count'] == 5]
    df4 = df.loc[df['Match_count'] == 4]
    df3 = df.loc[df['Match_count'] == 3]
    df2 = df.loc[df['Match_count'] == 2]
    df1 = df.loc[df['Match_count'] == 1]
    df0 = df.loc[df['Match_count'] == 0]

    df5.insert(0, "Rank", [*range(1, len(df5)+1)]) 
    df4.insert(0, "Rank", [*range(1, len(df4)+1)]) 
    df3.insert(0, "Rank", [*range(1, len(df3)+1)]) 
    df2.insert(0, "Rank", [*range(1, len(df2)+1)]) 
    df1.insert(0, "Rank", [*range(1, len(df1)+1)]) 
    df0.insert(0, "Rank", [*range(1, len(df0)+1)]) 
    
    df5.drop(['Match_count'], axis=1, inplace=True)
    df4.drop(['Match_count'], axis=1, inplace=True)
    df2.drop(['Match_count'], axis=1, inplace=True)
    df3.drop(['Match_count'], axis=1, inplace=True)
    df1.drop(['Match_count'], axis=1, inplace=True)
    df0.drop(['Match_count'], axis=1, inplace=True)

    return render(request, 'jobads/ranking.html', {'df5': df5, 'df4': df4, 'df3': df3, 'df2': df2, 'df1': df1, 'df0': df0, 'job_list': job_list, 'jobads': jobads})
