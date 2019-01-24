from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.views import Response
from rest_framework import viewsets, generics, status
from sap.models import Student, College, Course, Teacher, Attendance, Room
from .serializers import StudentSerializer, CollegeSerializer, CourseSerializer, TeacherSerializer, \
    AttendanceSerializer, RoomSerializer, ScheduleSerializer, CourseWithStatsSerializer
from django.forms.models import model_to_dict
import datetime
from datetime import timedelta


class StudentView(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    http_method_names = ['get', 'post', 'head', 'put']


class CollegeView(viewsets.ModelViewSet):
    serializer_class = CollegeSerializer
    queryset = College.objects.all()


class CourseView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class GetOneCourse(generics.ListAPIView):
    serializer_class = CourseWithStatsSerializer

    def get_queryset(self):
        return Course.objects.filter(pk=self.kwargs['courseid'])


class TeacherView(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class RoomView(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class ScheduleView(generics.ListAPIView):
    serializer_class = ScheduleSerializer

    # pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        today_min_5 = datetime.datetime.today() - timedelta(days=5)
        today_plus_30 = datetime.datetime.today() + timedelta(days=180)
        teacher = self.kwargs['userid']
        return College.objects.filter(teacher_id=teacher, day__gte=today_min_5.strftime("%Y-%m-%d"),
                                      day__lte=today_plus_30.strftime("%Y-%m-%d")).order_by('day')


class TeachersCoursesView(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        return Course.objects.filter(teacher=self.kwargs['teacherid'])


class AttendanceSummaryView(generics.ListAPIView):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        attendees = []
        college_id = self.kwargs['collegeid']
        college = College.objects.get(id=college_id)
        college_attendees = college.course.attendees.all()
        present_attendees = Attendance.objects.filter(college_id=college_id)
        for attendee in college_attendees:
            if present_attendees.all().filter(student_id=attendee.pk).exists():
                attendees.append(present_attendees.all().filter(student_id=attendee.pk).get())
            else:
                attendees.append({
                    'student': attendee,
                    'phone_check': False,
                    'card_check': False,
                    'student_course_stats': Course.course_stats_for_student(student=attendee, course=college.course)
                })
        return attendees


@api_view(['PUT'])
def set_attendance_student(self, collegeid, studentid):
    def attendance_timewindow_valid(college):
        if str(college.day) < str_date or str(college.day) > str_date:
            context = {"errormsg": "It is not allowed to set the attendance before or after the college day."}
            return Response(context, status=status.HTTP_403_FORBIDDEN)

    def check_serializer(serializer):
        if serializer.is_valid():
            serializer.save()
            context = {"success": "student succesfully saved"}
            return Response(context, status=status.HTTP_200_OK)

    def internal_server_error():
        context = {"errormsg": "Something went wrong during saving please try again or contact the system admin"}
        return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        dt = datetime.datetime.today()
        str_date = dt.strftime("%Y-%m-%d")
        student = Student.objects.filter(student_nr=studentid).get()
        college = College.objects.filter(pk=collegeid).get()
        window_check = attendance_timewindow_valid(college)
        if window_check:
            return window_check
        if Attendance.objects.filter(student_id=student.pk, college_id=collegeid).last():
            attendance = Attendance.objects.filter(student_id=student.pk, college_id=collegeid).last()
            if attendance.phone_check is True or attendance.card_check is True:
                attendance.delete()
                context = {"success": "student succesfully saved"}
                return Response(context, status=status.HTTP_200_OK)
            else:
                updated_attendance = Attendance(student=student, phone_check=True, card_check=True,
                                                college_id=collegeid)
                serializer = AttendanceSerializer(attendance, data=model_to_dict(updated_attendance))

                check_serializer = check_serializer(serializer)
                if check_serializer:
                    return check_serializer
            return internal_server_error()
        else:
            confirmed_attendance = Attendance(student=student, phone_check=True, card_check=True, college_id=collegeid)
            window_check = attendance_timewindow_valid(college)
            if window_check:
                return window_check
            confirmed_attendance.save()
            context = {"success": "student succesfully saved"}
            return Response(context, status=status.HTTP_200_OK)

    except Student.DoesNotExist or Teacher.DoesNotExist:
        context = {"errormsg": "Student does not exist"}
        return Response(context, status=status.HTTP_404_NOT_FOUND)
