from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from sap.models import Student, Collage
from .serializers import StudentSerializer, CollegeSerializer


class StudentView(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    http_method_names = ['get', 'post', 'head', 'put']


class CollegeView(viewsets.ModelViewSet):
    queryset = Collage.objects.all()
    serializer_class = CollegeSerializer

