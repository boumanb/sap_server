from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView, Response
from rest_framework import viewsets, permissions, generics
from sap.models import Student, Collage, Course, Teacher, Attendance, Room
from .serializers import StudentSerializer, CollegeSerializer, CourseSerializer, TeacherSerializer, \
    AttendanceSerializer, RoomSerializer
import datetime


class StudentView(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    http_method_names = ['get', 'post', 'head', 'put']


class CollegeView(viewsets.ModelViewSet):
    serializer_class = CollegeSerializer
    queryset = Collage.objects.all()


class CourseView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class TeacherView(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class AttendanceView(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


class RoomView(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class ScheduleView(generics.ListAPIView):
    serializer_class = CollegeSerializer

    def get_queryset(self):
        dt = datetime.datetime.today()
        str_time = dt.strftime("%H:%M:%S")
        str_date = dt.strftime("%Y-%m-%d")
        username = self.kwargs['userid']
        return Collage.objects.filter(teacher_id=username, day=str_date, begin_time__gte=str_time,)
