from rest_framework import serializers
from sap.models import Student, Teacher, Attendance, Course, Collage, Room


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('student_nr', 'email', 'device', 'card_uid', 'name')


class CollegeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Collage
        fields = ('day', 'begin_time', 'end_time', 'room', 'course', 'teacher', 'attendees')


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'teacher', 'created_at', 'updated_at')


class AttendanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attendance
        fields = ('timestamp', 'student', 'college', 'phone_check', 'card_check', 'phone', 'card')


class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Teacher
        fields = ('name', 'email', 'created_at', 'updated_at')


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ('name', 'reader_UID')
