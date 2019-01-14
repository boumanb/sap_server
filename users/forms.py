from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from sap.models import Teacher


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class TeacherRegisterForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'email']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


class TeacherUpdateForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name']
