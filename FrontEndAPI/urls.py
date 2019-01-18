from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Students', views.StudentView)
router.register('Colleges', views.CollegeView, base_name='Colleges')
router.register('Courses', views.CourseView)
router.register('Teacher', views.TeacherView)
router.register('Rooms', views.RoomView)


urlpatterns = [
    path('', include(router.urls)),
    path('Schedules/<userid>/', views.ScheduleView.as_view()),
    path('Teacher/<teacherid>/Courses/', views.TeachersCoursesView.as_view()),
    path('Attendances/<collegeid>/', views.AttendanceSummaryView.as_view()),
    path('Course/<courseid>/', views.GetOneCourse.as_view()),
    path('SetAttendance/<collegeid>/<studentid>/', views.set_attendance_student),
]