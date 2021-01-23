from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import RegexValidator
from datetime import date

# Create your models here.

STATES_CHOICES = (
   ('Penang','Penang'),
   ('Kuala Lumpur','Kuala Lumpur'),
   ('Selangor','Selangor'),
   ('Kedah','Kedah'),
   ('Perlis','Perlis'),
   ('Perak','Perak'),
   ('Kelantan','Kelantan'),
   ('Terengganu','Terengganu'),
   ('Negeri Sembilan','Negeri Sembilan'),
   ('Melaka','Melaka'),
   ('Pahang','Pahang'),
   ('Sarawak','Sarawak'),
   ('Sabah','Sabah'),
   ('Johor','Johor'),
   ('Labuan','Labuan'),
   ('Putrajaya','Putrajaya'),
)

FIELD = (
    ('Accounting/Finance', 'Accounting/Finance'),
    ('Admin/Human Resources', 'Admin/Human Resources'),
    ('Sales/Marketing', 'Sales/Marketing'),
    ('Arts/Media/Communications', 'Arts/Media/Communications'),
    ('Services', 'Services'),
    ('Hotel/Restaurant', 'Hotel/Restaurant'),
    ('Education/Training', 'Education/Training'),
    ('Computer/Information Technology', 'Computer/Information Technology'),
    ('Engineering', 'Engineering'),
    ('Manufacturing', 'Manufacturing'),
    ('Building/Construction','Building/Construction'),
    ('Sciences', 'Sciences'),
    ('Healthcare', 'Healthcare'),
    ('Others', 'Others'),
)

CATEGORY_CHOICES = (
    ('Home','Home'),
    ('Office','Office'),
    ('Health & Fitness','Health & Fitness'),
    ('Event','Event'),
    ('Lesson','Lesson'),
)

TYPE_CHOICES =(
    ('Home',(
        ('catering','Catering'),
        ('cleaning','Cleaning'),
        ('Plumbing','Plumbing'),
        ('Pet grooming','Pet grooming'),
        ('Lighting & Wiring','Lighting & Wiring'),
        ('Renovation & Improvement','Renovation& Improvement'),
    )),
    ('Office',(
        ('Pest Control','Pest Control'),
        ('Office Maintenance','Office Maintenance'),
        ('Office Space Rental','Office Space Rental'),
        ('Hardware/Software Support','Hardware/Software Support'),
    )),
    ('Event',(
        ('Catering','Catering'),
        ('Wedding','Wedding'),
        ('Entertainment','Entertainment'),
        ('Beauty & Salon','Beauty & Salon'),
        ('Photographers & Videographers','Photographer & Videographers'),
    )),
    ('Lessons',(
        ('Academic','Academic'),
        ('Language','Language'),
        ('Lifestyle & Hobby','Lifestyle & Hobby'),
    )),
    ('Health & Fitness',(
        ('Personal Training','Personal Training'),
        ('Rehabilitation & Wellness','Rehabilitation & Wellness'),
    ))
)

GRADE = (
    ('Grade A','Grade A'),
    ('Grade B','Grade B'),
    ('Grade C','Grade C'),
    ('Grade D','Grade D'),
    ('1st Class','1st Class'),
    ('2nd Class Upper','2nd Class Upper'),
    ('2nd Class Lower','2nd Class Lower'),
    ('3rd Class','3rd Class'),
    ('Pass/Non-gradable','Pass/Non-gradable'),
    ('Fail','Fail'),
    ('Incomplete','Incomplete'),
    ('On-going','On-going'),

)

POST_LEVEL =(
    ('Senior Manager','Senior Manager'),
    ('Manager','Manager'),
    ('Senior Executive','Senior Executive'),
    ('Junior Executive','Junior Executive'),
    ('Fresh / Entry Level','Fresh / Entry Level'),
    ('Non-Executive','Non-Executive'),
)

QUALIFICATION =(
    ('Primary/Secondary School/SPM/O Level','Primary/Secondary School/SPM/O Level'),
    ('Higher Secondary/STPM/A Level/Pre-U','Higher Secondary/STPM/A Level/Pre-U'),
    ('Professional Certificate','Professional Certificate'),
    ('Diploma','Diploma'),
    ('Advanced/Higher/Graduate Diploma','Advanced/Higher/Graduate Diploma'),
    ('Bachelor Degree','Bachelor Degree'),
    ('Post Graduate Degree','Post Graduate Degree'),
    ('Professional Degree','Professional Degree'),
    ('Master Degree','Master Degree'),
    ('Doctorate (PHD)','Doctorate (PHD)'),

)



class Employee(models.Model):
    name = models.CharField(max_length=100, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    address = models.CharField(max_length=1000, default='')
    city = models.CharField(max_length=1000, default='')
    nationality = models.CharField(max_length = 1000,default='')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_Number = models.CharField(validators=[phone_regex], max_length=13, default= '')
    skills = models.CharField(max_length=1000, default='',blank='True')
    languages = models.CharField(max_length=1000, default='',blank='True')
    prefered_work_location = models.CharField(max_length=1000,choices=STATES_CHOICES, default='',blank='True')
    expected_salary = models.IntegerField(blank='True',default=0)
    resume = models.FileField(upload_to='',default='',blank=True,null=True)
    # uploaded_at = models.DateTimeField(auto_now_add=True,default='')
    full_time = models.BooleanField(default=True)
    part_time = models.BooleanField(default=True)
 
    def __str__(self):
       return str(self.user.id)

class Employee_Edu(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    university = models.CharField(max_length=100,default='',blank='True')
    university_location = models.CharField(max_length=100,default='',blank='True')
    graduation_date = models.CharField(blank='True',max_length=20)
    qualification = models.CharField(choices= QUALIFICATION,max_length=100, default='',blank='True')
    field_of_study = models.CharField(choices= FIELD,max_length=100, default='',blank='True')
    title = models.CharField(max_length=100,default='',blank='True')
    grade = models.CharField(choices= GRADE,max_length=100, default='',blank='True')

    def __str__(self):
        return str(self.user.id)

class Employee_Exp(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    position_title = models.CharField(max_length=1000,default='',blank='True')
    company_name = models.CharField(max_length=1000,default='',blank='True')
    country = models.CharField(max_length=1000, default='',blank='True')  
    state = models.CharField(max_length=1000, default='',blank='True')  
    duration = models.CharField(blank='True',default='',max_length=1000)
    specialization = models.CharField(choices= FIELD,max_length=1000, default='',blank='True')
    industry = models.CharField(max_length=1000,default='',blank='True')
    position_level = models.CharField(choices= POST_LEVEL,max_length=1000, default='',blank='True')
    description = models.CharField(max_length=10000,default='',blank='True')
    
    def __str__(self):
        return str(self.user.id)      

class Freelancer(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE,default=1)
    contact_person_name = models.CharField(max_length=100, default='')
    registered_business_name = models.CharField(max_length=100, default='')
    registration_number = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=500,null=True,blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_Number = models.CharField(validators=[phone_regex], max_length=13, default= '')
    category = models.CharField(max_length=100,choices = CATEGORY_CHOICES, default='',blank ='True')
    service_type = models.CharField(max_length=100,choices = TYPE_CHOICES, default='',blank ='True')
    services_offer = models.CharField(max_length=500,null=True,blank=True)
    description = models.CharField(max_length=500,null=True,blank=True)
    city = models.CharField(max_length=100, default='',null=True,blank=True)
    

    def __str__(self):
        return str(self.user.id)

