from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
import requests
from django.http import JsonResponse, HttpResponse
import datetime

api_url = "http://127.0.0.1:8000/api"


# Index method returns only the colleges on the current day
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
    for sch in schedules['results']:
        if sch['day'] == str_date and sch['begin_time'] >= str_time:
            t_list.append(sch)

    context = {
        'schedules': t_list,
    }
    return render(request, 'teacherportal/index.html', context)


# Schedule shows all planned colleges on current day and after that
@login_required
def schedule(request):
    user = request.user
    number = str(request.GET.get('page', '1'))
    token = Token.objects.get(user=user)
    get_schedule = requests.get(
        api_url + '/Schedules/' + str(user.teacher.pk) + '/?page=' + number,
        headers={'Authorization': 'token ' + token.key})
    schedules = get_schedule.json()
    page_next = None
    page_previous = None

    if schedules['next']:
        page_next = get_page_number(schedules['next'])

    if schedules['previous']:
        page_previous = get_page_number(schedules['previous'])

    context = {
        'schedules': schedules['results'],
        'count': schedules['count'],
        'next': page_next,
        'previous': page_previous,
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
    # Go to function def check_teacher to check if the teacher is the one that the college is linked to.
    teacher_check = check_teacher(user, collegeid)

    if teacher_check:
        context = {
            'attendances': attendances,
            'collegeid': collegeid,
        }
        return render(request, 'teacherportal/attendance_summary.html', context)
    else:
        return HttpResponse('Unauthorized', status=401)


# Set the student attendance from false to true
@login_required
def set_student_attendance(request, collegeid, studentid):
    user = request.user
    token = Token.objects.get(user=user)

    # Go to function def check_teacher to check if the teacher is the one that the college is linked to.
    teacher_check = check_teacher(user, collegeid)

    if teacher_check:
        set_attendance = requests.put(api_url + '/SetAttendance/' + str(collegeid) + '/' + str(studentid) + '/',
                                      headers={'Authorization': 'token ' + token.key})
        data = set_attendance.json()
        if data['success']:
            return JsonResponse(data)
        else:
            return JsonResponse(data)
    else:
        return HttpResponse('Unauthorized', status=401)


# Checks if the teacher is the one of the current college
def check_teacher(user, collegeid):
    token = Token.objects.get(user=user)
    teacher_check = requests.get(api_url + '/Courses/' + collegeid + '/',
                                 headers={'Authorization': 'token ' + token.key}).json()
    teachers = teacher_check['teacher']
    for teacher in teachers:
        if teacher == user.teacher.pk:
            return True
        else:
            return False


# return the page number from the URL so this can be used as a HREF in the template
def get_page_number(url):
    a, *page_number = url.split('=', 1)
    if page_number:
        return str(page_number[0])
    else:
        return str(1)


# Custom 404 for the teacherportal
def handler404(request):
    data = {}
    return render(request, '404.html', data)


# Custom 500 internal error for the teacherportal
def handler500(request):
    data = {}
    return render(request, '500.html', data)
