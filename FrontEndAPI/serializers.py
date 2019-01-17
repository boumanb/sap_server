from rest_framework import serializers
from sap.models import Student, Teacher, Attendance, Course, College, Room


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('student_nr', 'email', 'device', 'card_uid', 'name')


class CollegeSerializer(serializers.ModelSerializer):
    room = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name'
    )
    course = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = College
        fields = ('day', 'begin_time', 'end_time', 'room', 'course', 'teacher', 'attendees')


class CourseSerializer(serializers.ModelSerializer):
    teacher = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='id'
    )

    class Meta:
        model = Course
        fields = ('id', 'name', 'teacher', 'created_at', 'updated_at')


class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer(many=False, read_only=True)

    class Meta:
        model = Attendance
        fields = ('timestamp', 'student', 'college', 'phone_check', 'card_check', 'phone', 'card', 'student_id', 'course_stats')


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('name', 'email', 'created_at', 'updated_at')


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('name', 'reader_UID')


class ScheduleSerializer(serializers.ModelSerializer):
    room = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name'
    )
    course = CourseSerializer(many=False, read_only=True)

    class Meta:
        model = College
        fields = ('id', 'day', 'begin_time', 'end_time', 'room', 'course', 'teacher')
