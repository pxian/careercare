import os
import docx2txt
import pdfplumber
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from gensim.summarization.summarizer import summarize
from pyresparser import ResumeParser
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .forms import *
from .models import *
from .utils import *

# @login_required(login_url='/employers/login/')
def index(request):
    return render(request, "index.html")


def register(request):
    if request.method == "POST":
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data.get("username")
            password = register_form.cleaned_data.get("password1")
            user = User.objects.create_user(
                username=username, password=password)
            user.save()
            messages.info(request, "Thank you for registering.")
            auth_login(request, user)
            return redirect("login")
    else:
        register_form = UserCreationForm()
    return render(request, "register.html", {"form": register_form})


def login(request):
    if request.method == "POST":
        log_in_form = AuthenticationForm(data=request.POST)
        if log_in_form.is_valid():
            user = log_in_form.get_user()
            auth_login(request, user)
            messages.add_message(request, messages.INFO, "Log in successfully.")
            return redirect("index")
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect("login")
    else:
        log_in_form = AuthenticationForm()
    return render(request, "login.html", {"form": log_in_form})


def logout(request):
    auth.logout(request)
    messages.add_message(request,messages.INFO,"Logged out successfully.")
    return redirect("index")


def uploadresume(request):
    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES)
        files = request.FILES.getlist("resume")
        if form.is_valid():
            for file in files:
                try:
                    resume = Resume(resume=file)
                    resume.user = request.user
                    resume.save()
                    parser = ResumeParser(os.path.join(settings.MEDIA_ROOT, resume.resume.name))
                    data = parser.get_extracted_data()
                    resume.name = data.get("name")
                    if data.get("email") is not None:
                        resume.email = data.get("email")
                    else:
                        resume.email = None
                        messages.warning(request, "Email is not found in " + file.name + ", please review resume and add in the required information.")
                    if data.get("mobile_number") is not None:
                        resume.mobile_number = data.get("mobile_number")
                    else:
                        resume.mobile_number = None
                        messages.warning(request, "Mobile number is not found in " + file.name + ", please review resume and add in the required information.")
                    if data.get("experience") is not None:
                        resume.experience = '\n '.join(data.get("experience"))
                    else:
                        resume.experience = None
                    if data.get("education") is not None:
                        resume.education = '\n '.join(data.get("education"))
                    else:
                        resume.education = None
                    if data.get("skills") is not None:
                        resume.skills = '\n '.join(data.get("skills"))
                    else:
                        resume.skills = None
                    if data.get("designation") is not None:
                        resume.designation = '\n '.join(data.get("designation"))
                    else:
                        resume.designation = None
                    if data.get("company_names") is not None:
                        resume.company_name = '\n '.join(data.get("company_names"))
                    else:
                        resume.company_name = None

                    text = file.open()
                    if resume.extension() == "docx":
                        text = docx2txt.process(text)
                        text = str(text)
                    elif resume.extension() == "pdf":
                        content = ""
                        with pdfplumber.open(text) as pdf:
                            for page in pdf.pages:
                                text = page.extract_text()
                                content += text
                            text = str(content)
                    resume.summary = summarize(str(text), ratio=0.01)
                    resume.save()
                except ValidationError:
                    messages.warning(request, "Duplicate resume found: " + file.name)
                    return redirect("resumeanalyzer:uploadresume")
                except IntegrityError:
                    messages.warning(request, "Encountered a problem with the file, please try again.")
                    return redirect("resumeanalyzer:uploadresume")
            messages.add_message(request, messages.INFO, "Resume(s) uploaded successfully.")
            return redirect("resumeanalyzer:resumelist")
        else:
            form = ResumeForm()
            messages.warning(request, "Please select file.")
    else:
        form = ResumeForm()
    return render(request, "uploadresume.html", {"form": form})


def resumelist(request):
    resumes = Resume.objects.all()
    return render(request, "resumelist.html", {"resumes": resumes})


def uploadjob(request):
    if request.method == "POST":
        form = JobDescForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                title = form.cleaned_data["title"]
                jobdesc = request.FILES.get("jobdesc")
                if jobdesc.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    jobdesc = docx2txt.process(jobdesc)
                    jobdesc = str(jobdesc)
                elif jobdesc.content_type == "application/pdf":
                    content = ""
                    with pdfplumber.open(jobdesc) as pdf:
                        for page in pdf.pages:
                            text = page.extract_text()
                            content += text
                        jobdesc = str(content)
                summary = summarize(jobdesc, ratio=0.1)
                job = form.save(commit=False)
                job.summary = summary
                job.title = title
                job.user = request.user
                job.save()
                form.save()
                messages.add_message(request, messages.INFO, "Job description uploaded successfully.")
            except ValidationError:
                messages.warning(request, "Duplicate job description found.")
                form = JobDescForm()
                return render(request, "uploadjob.html", {"POST": False, "form": form})
            except IntegrityError:
                messages.warning(request, "Please fill in the form completely.")
                form = JobDescForm()
                return render(request, "uploadjob.html", {"POST": False, "form": form})
            return redirect("resumeanalyzer:matchall", jobid=job.jobid)
        else:
            form = JobDescForm()
            messages.warning(request, "Please fill in the form completely.")
    else:
        form = JobDescForm()
    return render(request, "uploadjob.html", {"POST": False, "form": form})


def matchall(request, jobid):
    dict = {}
    job = JobDesc.objects.get(jobid=jobid)
    title = job.title
    jobdesc = job.jobdesc.open()
    if job.extension() == "docx":
        jobdesc = docx2txt.process(jobdesc)
        jobdesc = str(jobdesc)
    elif job.extension() == "pdf":
        content = ""
        with pdfplumber.open(jobdesc) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                content += text
            jobdesc = str(content)
    resumes = Resume.objects.filter(resume__isnull=False)
    for file in resumes:
        resume = file.resume.open()
        if file.extension() == "docx":
            resume = docx2txt.process(resume)
            resume = str(resume)
        elif file.extension() == "pdf":
            content = ""
            with pdfplumber.open(resume) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    content += text
                resume = str(content)
        text = [resume, jobdesc]
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(text)
        percentage = cosine_similarity(count_matrix)[0][1] * 100
        percentage = round(percentage, 2)
        percentage = "{:.2f}".format(percentage)
        dict[file] = percentage
        Result.objects.get_or_create(user = request.user, jobid_id = job.jobid, resumeid_id = file.resumeid, percentage = percentage)
    sorted_dict = {}
    sorted_keys = sorted(dict, key=dict.get, reverse = True)
    for j in sorted_keys:
        sorted_dict[j] = dict[j]
    return render(request, "match.html", {"title": title, "sorted_dict": sorted_dict, "job":job, "resumes": resumes})


def matchshortlisted(request, jobid):
    dict = {}
    job = JobDesc.objects.get(jobid=jobid)
    title = job.title
    jobdesc = job.jobdesc.open()
    if job.extension() == "docx":
        jobdesc = docx2txt.process(jobdesc)
        jobdesc = str(jobdesc)
    elif job.extension() == "pdf":
        content = ""
        with pdfplumber.open(jobdesc) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                content += text
            jobdesc = str(content)
    resumes = Resume.objects.filter(status="Shortlisted")
    for file in resumes:
        resume = file.resume.open()
        if file.extension() == "docx":
            resume = docx2txt.process(resume)
            resume = str(resume)
        elif file.extension() == "pdf":
            content = ""
            with pdfplumber.open(resume) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    content += text
                resume = str(content)
        text = [resume, jobdesc]
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(text)
        percentage = cosine_similarity(count_matrix)[0][1] * 100
        percentage = round(percentage, 2)
        percentage = "{:.2f}".format(percentage)
        dict[file] = percentage
    sorted_dict = {}
    sorted_keys = sorted(dict, key=dict.get, reverse = True)
    for j in sorted_keys:
        sorted_dict[j] = dict[j]
    return render(request, "match.html", {"title": title, "sorted_dict": sorted_dict, "job": job, "resumes": resumes})


def filter(request, jobid):
    form = Filter(request.POST)
    job = JobDesc.objects.get(jobid=jobid)
    if request.method == "POST":
        if form.is_valid():
            selected = form.cleaned_data["filter"]
            if selected=="all":
                return redirect("resumeanalyzer:matchall", jobid=jobid)
            else:
                return redirect("resumeanalyzer:matchshortlisted", jobid=jobid)
    return render(request, "result.html", {"job": job, "form": form})


def details(request, resumeid):
    file = Resume.objects.filter(resumeid=resumeid)
    resume = get_object_or_404(file, resumeid=resumeid)
    results = Result.objects.filter(resumeid_id=resumeid)
    return render(request, "details.html", {"resume": resume, "results": results})


def addNotes(request, resumeid):
    resume = Resume.objects.get(resumeid=resumeid)
    if request.method == "POST":
        resume.note = request.POST['note']
        resume.save(update_fields=['note'])
        messages.add_message(request, messages.INFO, "Notes updated successfully.")
        return render(request, "details.html", {"resume": resume})
    else:
        messages.warning(request, "You did not make any changes.")
        return render(request, "details.html", {"resume": resume})


def deleteResume(request, resumeid):
    if request.method == "POST":
        Resume.objects.filter(resumeid=resumeid).delete()
        messages.add_message(request, messages.INFO, "Resume deleted successfully.")
        return redirect("resumeanalyzer:resumelist")
    else:
        return redirect("resumeanalyzer:resumelist")


def deleteJob(request, jobid):
    if request.method == "POST":
        JobDesc.objects.filter(jobid=jobid).delete()
        messages.add_message(request, messages.INFO, "Job deleted successfully.")
        return redirect("resumeanalyzer:history")
    else:
        return redirect("resumeanalyzer:history")


def history(request):
    jobdesc = JobDesc.objects.all()
    return render(request, "history.html", {"jobdesc": jobdesc})


def result(request, jobid):
    job = JobDesc.objects.get(jobid=jobid)
    results = Result.objects.filter(jobid_id=jobid)
    for result in results:
        title = result.jobid.title
        return render(request, "result.html", {"title": title, "results": results, "job": job})


def shortlist(request, resumeid):
    if request.method == "POST":
        resume = Resume.objects.get(resumeid=resumeid)
        resume.shortlist()
        messages.add_message(request, messages.INFO, "Successfully shortlisted.")
        return render(request, "details.html", {"resume": resume})
    else:
        return render(request, "details.html")


def delist(request, resumeid):
    if request.method == "POST":
        resume = Resume.objects.get(resumeid=resumeid)
        resume.delist()
        messages.add_message(request, messages.INFO, "Successfully delisted.")
        return render(request, "details.html", {"resume": resume})
    else:
        return render(request, "details.html")


def visualise(request, jobid):
    results = Result.objects.filter(jobid_id=jobid)
    job = JobDesc.objects.get(jobid=jobid)
    x = [x.resumeid.name for x in results]
    y = [y.percentage for y in results]
    chart = get_plot(x,y)
    return render(request, "visualise.html", {"chart": chart, "job": job})


def visualiseshortlisted(request, jobid):
    results = Result.objects.filter(jobid_id=jobid, resumeid__status="Shortlisted")
    job = JobDesc.objects.get(jobid=jobid)
    x = [x.resumeid.name for x in results]
    y = [y.percentage for y in results]
    chart = get_plot(x,y)
    return render(request, "visualise.html", {"chart": chart, "job": job})


def visualisefilter(request, jobid):
    form = Filter(request.POST)
    job = JobDesc.objects.get(jobid=jobid)
    if request.method == "POST":
        if form.is_valid():
            selected = form.cleaned_data["filter"]
            if selected=="all":
                return redirect("resumeanalyzer:visualise", jobid=jobid)
            else:
                return redirect("resumeanalyzer:visualiseshortlisted", jobid=jobid)
    return render(request, "visualise.html", {"job": job, "form": form})
