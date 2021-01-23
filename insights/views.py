import sys
# from nltk.corpus import stopwords
from collections import Counter
import pandas as pd
import plotly.figure_factory as ff
from django.apps import apps
# import re
# import string
# import plotly
# import operator
# from functools import reduce
# import plotly.graph_objs as go
# from plotly.offline import plot
from django.db.models import Count, Q, Sum
from django.shortcuts import render
# matplotlib.use('Agg')
from matplotlib import pyplot as plt

# import mpld3
# import json
# from io import BytesIO
# import base64
# jobskills_df = pd.read_csv(r"C:\Users\user\Desktop\Technology_Skills.csv")

# Create your views here.
def insights(request):
    jobviewed = viewed_job(request)
    astatus = app_status(request)
    # jobmatch = skill_job(request)
    return render(request, 'insights/insights.html',{'jobviewed':jobviewed,'astatus':astatus})


def app_status(request):
    Application = apps.get_model('searchjob','AppliedJob')
    appstatus = Application.objects.filter(user_id=request.user.id).values('status').annotate(count= Count('status'))
    
    return appstatus




def viewed_job(request):
    viewed = apps.get_model('searchjob','ViewedJob')
    viewedjob = viewed.objects.filter(user_id=request.user.id).select_related('jobad').order_by('-timestamp')[:5]
    return viewedjob

# class skill_keyword_match:
#     def __init__(self, jobskills_df):
#         self.df = pd.DataFrame(jobskills_df)
   
#     def get_jaccard_sim(self, x_set, y_set):
#         intersection = x_set.intersection(y_set)
#         return float(len(intersection)) / (len(x_set) + len(y_set) - len(intersection))

#     def cal_similarity(self, myskills):
#         num_jobs_return = 5
#         similarity = []
#         j_info = self.df.copy()
#         if j_info.shape[0] < num_jobs_return:        
#             num_jobs_return = j_info.shape[0]  
#         for job_skills in j_info['Example']:
#             similarity.append(self.get_jaccard_sim(set(myskills), set(job_skills)))
#         j_info['similarity'] = similarity
#         j_info['Title']= jobskills_df['Title']
#         top_match = j_info.sort_values(by='similarity', ascending=False).head(num_jobs_return)        
#         # Return top matched jobs
#         return top_match 

# plt.ioff()    
# def skill_job(request):
#     myskills = "Java, Python, R, PHP, HTML, CSS, XML, Javascript, Bootstrap, Django, SQL, mySQL, sqlite, MS SQL, MongoDB, C#, C++, Hadoop, ASP.NET, AJAX, Apache"
#     job_skills = jobskills_df['Example']

#     skill_match = skill_keyword_match(job_skills)


#     top_job_matches = skill_match.cal_similarity(myskills)
#     # fig = plt.figure()
#     job = top_job_matches.sort_values('similarity')
#     x = job['Title']
#     y = job['similarity']
#     fig = plt.figure()
#     plt.barh(x,y,color="grey")
#     buf=BytesIO()
#     plt.savefig(buf,format='png')
#     image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
#     buf.close()
#     # single_chart['id'] = "fig_01"
#     # single_chart=dict()
#     # single_chart['json'] = json.dumps(mpld3.fig_to_dict(fig))
#     # result={'single_chart':single_chart}
#     # plt.show()
#     #plt.close()
#     #return image
#     # return single_chart
