from django.contrib.auth import views as auth_views
from django.conf.urls import handler404, handler500
from django.urls import path, include
from users import views as user_views
from . import views


urlpatterns = [
     path('', views.index, name="teacherportal-home"),
     path('register/', user_views.register, name="register"),
     path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name="login"),
     path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
     path('activate/<uidb64>/<token>', user_views.activate, name="activate"),
     path('teacher/', user_views.teacher, name="teacher"),
     path('teacher/teacher_edit', user_views.teacher_edit, name="teacher_edit"),

     path('today_schedule/', views.today_schedule, name="today_schedule"),
     path('schedule/', views.schedule, name="schedule"),
     path('stats/', views.stats, name="stats"),
     path('attendance_summary/<collegeid>/', views.get_attendance_summary, name="attendance_summary"),
     path('set_student_attendance/<collegeid>/<studentid>/', views.set_student_attendance, name="set_student_attendance")


]

handler404 = views.handler404
handler500 = views.handler500