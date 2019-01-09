from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
import requests
from django.http import JsonResponse, HttpResponse
import datetime

api_url = "http://127.0.0.1:8000/api"
tokens = '123'


# get_students = requests.get(api_url + '/Students', headers={'Authorization': 'token ' + token.key})
# students = get_students.json()
# Get students
# Index method returns only the colleges on the current day the teacher makes the request
@login_required
def index(request):
    user = request.user
    token = Token.objects.get(user=user)
    get_schedule = requests.get(api_url + '/Schedules/' + str(user.teacher.pk) + '/',
                                headers={'Authorization': 'token ' + token.key})
    schedules = get_schedule.json()
    dt = datetime.datetime.today()
    str_date = dt.strftime("%Y-%m-%d")
    str_time = dt.strftime("%H:%M:%S")
    t_list = []
    for schedule in schedules:
        if schedule['day'] == str_date and schedule['begin_time'] >= str_time:
            t_list.append(schedule)

    context = {
        'schedules': t_list,
    }
    return render(request, 'teacherportal/index.html', context)


# path('/schedules/?P<userid>.+/$'), # str_time = dt.strftime("%H:%M:%S"), str_date = dt.strftime("%Y-%m-%d")
# Schedule shows all planned colleges on current day and after
@login_required
def schedule(request):
    user = request.user
    token = Token.objects.get(user=user)
    get_schedule = requests.get(api_url + '/Schedules/' + str(user.teacher.pk) + '/',
                                headers={'Authorization': 'token ' + token.key})
    schedules = get_schedule.json()
    dt = datetime.datetime.today()
    str_date = dt.strftime("%Y-%m-%d")
    f_list = []
    for schedule in schedules:
        if schedule['day'] >= str_date:
            f_list.append(schedule)
    context = {
        'schedules': f_list,
    }
    return render(request, 'teacherportal/schedule.html', context)


# get the attendance of all the students that should be in the college
@login_required
def get_attendance_summary(request, collegeid):
    user = request.user
    token = Token.objects.get(user=user)
    get_attendance = requests.get(api_url + '/Attendances/' + str(collegeid) + '/',
                                  headers={'Authorization': 'token ' + token.key})
    attendances = get_attendance.json()

    teacher_check = requests.get(api_url + '/Courses/' + collegeid + '/',
                                 headers={'Authorization': 'token ' + token.key}).json()
    teachers = teacher_check['teacher']
    for teacher in teachers:
        if teacher == user.teacher.pk:
            context = {
                'attendances': attendances,
                'collegeid': collegeid,
            }
            return render(request, 'teacherportal/attendance_summary.html', context)
        else:
            return HttpResponse('Unauthorized', status=401)


@login_required
def set_student_attendance(request, collegeid, studentid):
    user = request.user
    token = Token.objects.get(user=user)
    set_attendance = requests.put(api_url + '/SetAttendance/' + str(collegeid) + '/' + str(studentid) + '/',
                                  headers={'Authorization': 'token ' + token.key})
    data = set_attendance.json()
    if data['success']:
        return JsonResponse(data)
    else:
        return JsonResponse(data)


def handler404(request):
    data = {}
    return render(request, '404.html', data)


def handler500(request):
    data = {}
    return render(request, '500.html', data)


