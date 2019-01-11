from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.views import Response
from rest_framework import viewsets, generics, status
from sap.models import Student, Collage, Course, Teacher, Attendance, Room
from .serializers import StudentSerializer, CollegeSerializer, CourseSerializer, TeacherSerializer, \
    AttendanceSerializer, RoomSerializer, ScheduleSerializer
from django.forms.models import model_to_dict
import datetime


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


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


class RoomView(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class ScheduleView(generics.ListAPIView):
    serializer_class = ScheduleSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        dt = datetime.datetime.today()
        str_date = dt.strftime("%Y-%m-%d")
        teacher = self.kwargs['userid']
        return Collage.objects.filter(teacher_id=teacher, day__gte=str_date).order_by('pk')


class AttendanceSummaryView(generics.ListAPIView):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        collegeid = self.kwargs['collegeid']
        return Attendance.objects.filter(college_id=collegeid)


@api_view(['PUT'])
def set_attendance_student(self, collegeid, studentid):
    try:
        dt = datetime.datetime.today()
        str_date = dt.strftime("%Y-%m-%d")
        student = Student.objects.filter(student_nr=studentid).get()
        attend = Attendance.objects.filter(student_id=student.pk, college_id=collegeid).get()
        confirm = Attendance(student=student, phone_check=True, card_check=True, college_id=collegeid)
        serializer = AttendanceSerializer(attend, data=model_to_dict(confirm))
        college = Collage.objects.filter(pk=collegeid).get()
        if str(college.day) < str_date or str(college.day) > str_date:
            context = {"errormsg": "It is not allowed to set the attendance before or after the college day."}
            return Response(context, status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save()
            context = {"success": "student succesfully saved"}
            return Response(context, status=status.HTTP_200_OK)
        context = {"errormsg": "Something went wrong during saving please try again or contact the system admin"}
        return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Student.DoesNotExist or Teacher.DoesNotExist:
        context = {"errormsg": "Student does not exist"}
        return Response(context, status=status.HTTP_404_NOT_FOUND)
