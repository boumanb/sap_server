import requests
from django.test import TestCase, Client
from rest_framework.authtoken.models import Token
from rest_framework.utils import json
from sap.models import Teacher, College, Course, Room, Student
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import datetime
from datetime import timedelta


class FrontEndApiTest(TestCase):
    url = "http://127.0.0.1:8000/api/"

    def setUp(self):
        dt = datetime.datetime.today()
        df = dt + timedelta(days=1)
        str_date_extent = df.strftime("%Y-%m-%d")
        str_date = dt.strftime("%Y-%m-%d")
        str_time = dt.strftime("%H:%M:%S")
        user = User.objects.create(username="jaap", password='@Welkom1')
        teacher = Teacher.objects.create(name="Jaap", email="Jaap@hr.nl", user=user)
        token = Token.objects.create(user=user)
        room = Room.objects.create(name="404", reader_UID="123456")
        student1 = Student.objects.create(name="Peter Pannekoek", student_nr="123456", email="peter@hr.nl",
                                          card_uid="654321")
        student2 = Student.objects.create(name="Willem Waan", student_nr="736423", email="willem@hr.nl",
                                          card_uid="847463")
        course = Course.objects.create(name="Biep")
        course.teacher.add(teacher)
        course.attendees.add(student1)
        course.attendees.add(student2)
        college = College.objects.create(day=str_date, begin_time="21:00:00", end_time="22:00:00", room=room,
                                         course_id=course.pk, teacher_id=teacher.pk)
        college.attendees.add(student1)
        college.attendees.add(student2)
        college2 = College.objects.create(day=str_date_extent, begin_time="16:00:00", end_time="18:00:00", room=room,
                                          course_id=course.pk, teacher_id=teacher.pk)
        college2.attendees.add(student1)
        college2.attendees.add(student2)

    def scheduleview_correct_teacher(self):
        user = User.objects.get(username="jaap")
        token = Token.objects.get(user__username='jaap')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(self.url + 'Schedules/' + str(user.teacher.pk) + '/', format='json')
        schedules = json.loads(response.content)

        assert str(schedules['results'][0]['teacher']) == '1'
        assert response.status_code == 200

    def set_student_attendance(self):
        user = User.objects.get(username='jaap')
        token = Token.objects.get(user__username='jaap')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.put(self.url + 'SetAttendance/' + str(1) + '/' + str(123456) + '/', format='json')
        attendance = json.loads(response.content)

        assert attendance['success'] == 'student succesfully saved'
        assert response.status_code == 200

    def set_student_attendance_wrong_day(self):
        user = User.objects.get(username='jaap')
        token = Token.objects.get(user__username='jaap')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.put(self.url + 'SetAttendance/' + str(2) + '/' + str(123456) + '/', format='json')
        attendance = json.loads(response.content)

        assert attendance['errormsg'] == 'It is not allowed to set the attendance before or after the college day.'
        assert response.status_code == 403
