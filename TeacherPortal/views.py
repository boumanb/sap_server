from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
import requests
from django.http import JsonResponse, HttpResponse
import datetime

from sap import settings
from sap.models import Course

api_url = settings.BASE_URL_W_TRAILING_SLASH + 'api/'


def index(request):
    if request.user.is_authenticated:
        return redirect('schedule')
    return redirect('login')


# Index method returns only the colleges on the current day
@login_required
def today_schedule(request):
    user = request.user
    token = Token.objects.get(user=user)
    get_schedule = requests.get(api_url + 'Schedules/' + str(user.teacher.pk) + '/',
                                headers={'Authorization': 'token ' + token.key})
    schedules = get_schedule.json()
    dt = datetime.datetime.today()
    str_date = dt.strftime("%Y-%m-%d")
    str_time = dt.strftime("%H:%M:%S")
    t_list = []
    for sch in schedules:
        if sch['day'] == str_date:
            t_list.append(sch)

    context = {
        'schedules': t_list,
    }
    return render(request, 'teacherportal/today_schedule.html', context)


# Schedule shows all planned colleges on current day and after that
@login_required
def schedule(request):
    return render(request, 'teacherportal/schedule.html')


# get the attendance of all the students that should be in the college
@login_required
def get_attendance_summary(request, collegeid):
    user = request.user
    token = Token.objects.get(user=user)
    get_attendance = requests.get(api_url + 'Attendances/' + str(collegeid) + '/',
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
        set_attendance = requests.put(api_url + 'SetAttendance/' + str(collegeid) + '/' + str(studentid) + '/',
                                      headers={'Authorization': 'token ' + token.key})
        return JsonResponse(set_attendance.json())
    else:
        return HttpResponse('Unauthorized', status=401)


@login_required
def stats(request, courseid=None):
    token = Token.objects.get(user=request.user)
    if not courseid:
        courses = requests.get(api_url + 'Teacher/' + str(request.user.teacher.pk) + '/Courses',
                               headers={'Authorization': 'token ' + token.key}).json()
        context = {
            'courses': courses
        }
        return render(request, 'teacherportal/courses.overview.html', context)
    else:
        if Course.objects.filter(pk=courseid).exists():
            course = Course.objects.get(pk=courseid)
            if course.teacher.filter(pk=request.user.teacher.pk).exists():
                course_stats = requests.get(api_url + 'Course/' + courseid,
                                            headers={'Authorization': 'token ' + token.key}).json()
                context = {
                    'course_stats': course_stats
                }
                return render(request, 'teacherportal/course.stats.html', context)
            else:
                return HttpResponse('Unauthorized', status=401)
        else:
            return HttpResponse('Course not found', status=404)


# Checks if the teacher is the one of the current college
def check_teacher(user, collegeid):
    token = Token.objects.get(user=user)
    teacher_check = requests.get(api_url + 'Colleges/' + collegeid + '/',
                                 headers={'Authorization': 'token ' + token.key}).json()
    if teacher_check['teacher'] is user.teacher.pk:
        return True
    else:
        return False


def check_teacher_course(user, course_id):
    pass


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
