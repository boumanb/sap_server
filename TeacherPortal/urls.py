from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
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


     path('schedule/', views.schedule, name="schedule")


]