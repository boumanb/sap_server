from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Students', views.StudentView)
router.register('Colleges', views.CollegeView, base_name='Colleges')
router.register('Courses', views.CourseView)
router.register('Teacher', views.TeacherView)
router.register('Attendances', views.AttendanceView)
router.register('Rooms', views.RoomView)


urlpatterns = [
    path('', include(router.urls)),
    path('Schedule/<userid>/', views.ScheduleView.as_view()),
]