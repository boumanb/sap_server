from django.shortcuts import render
from FrontEndAPI.serializers import StudentSerializer
from sap.models import Student
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
import requests
import datetime

api_url = "http://127.0.0.1:8000/api"
tokens = '123'


# get_students = requests.get(api_url + '/Students', headers={'Authorization': 'token ' + token.key})
# students = get_students.json()
# Get students

@login_required
def index(request):
    user = request.user
    token = Token.objects.get(user=user)

    return render(request, 'teacherportal/index.html')


# path('/schedules/?P<userid>.+/$'),
@login_required
def schedule(request):
    user = request.user
    token = Token.objects.get(user=user)
    get_schedule = requests.get(api_url + '/Schedule/' + str(user.teacher.pk) + '/')
    schedules = get_schedule.json()
    context = {
        'schedules': schedules,
    }
    return render(request, 'teacherportal/schedule.html', context)
