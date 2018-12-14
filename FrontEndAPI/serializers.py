from rest_framework import serializers
from sap.models import Student, Teacher, Attendance, Course, Collage, Room


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('student_nr', 'email', 'device', 'card_uid', 'name')


class CollegeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Collage
        fields = ('day', 'begin_time', 'end_time', 'room', 'course')


class AttendanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attendance
        fields = ('','')