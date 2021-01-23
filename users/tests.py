from django.test import TestCase
from .models import Employee,Employee_Edu,Employee_Exp
from django.contrib.auth.models import User
from .forms import ProfileForm,ExpFormSet,EduFormSet
# Create your tests here.

class CreateProfileTest(TestCase):

    def test_create_profile(self):
        data={
            'name':'Calvin Tan',
            'address':'2561, Sungai Udang, 14310 Nibong Tebal,Pulau Pinang',
            'city':'Nibong Tebal',
            'nationality':'Malaysian',
            'phone_Number':'0123456789',
            'skills':'Java, Python, PHP, Django, MYSQL, ASP.NET, CSS',
            'languages':'English,Malay,Mandarin',
            'prefered_work_location':'Penang',
            'expected_salary':3000,
            
        }
        form = ProfileForm(data)

        self.assertTrue(form.is_valid())

    def test_create_education(self):
        data={
            'EduFormSet-INITIAL_FORMS': '1',
            'EduFormSet-TOTAL_FORMS': '2',
            'EduFormSet-MAX_NUM_FORMS': '',

            'EduFormSet-0-university':'Universiti Malaya',
            'EduFormSet-0-university_location':'Kuala Lumpur',
            'EduFormSet-0-graduation_date':'Feb 2021',
            'EduFormSet-0-field_of_study':'Computer/Information Technology',
            'EduFormSet-0-title':'Bachelor in Computer Science (Information System)',
            

            'EduFormSet-1-university':'UM',
            'EduFormSet-1-university_location':'KL',
            'EduFormSet-1-graduation_date':'Feb 2020',
            'EduFormSet-1-field_of_study':'Computer/Information Technology',
            'EduFormSet-1-title':'Bachelor in Computer Science (IS)',
        }
        form = EduFormSet(data)
        form.is_valid(); print(form.errors)
        self.assertTrue(form.is_valid())

    def test_create_experience(self):
        data={
            'ExpFormSet-INITIAL_FORMS': '1',
            'ExpFormSet-TOTAL_FORMS': '2',
            'ExpFormSet-MAX_NUM_FORMS': '',

            'ExpFormSet-0-position_title':'Web Developer (Intern)',
            'ExpFormSet-0-company_name':'Vitrox Corporation',
            'ExpFormSet-0-country':'Malaysia',
            'ExpFormSet-0-state':'Penang',
            'ExpFormSet-0-duration':'Jan 2020 - Aug 2020',
            'ExpFormSet-0-industry':'Electronics',
            'ExpFormSet-0-description':'Had internship for 8 months. Responsible in web developing.',
        }
        form = ExpFormSet(data)
        self.assertTrue(form.is_valid())