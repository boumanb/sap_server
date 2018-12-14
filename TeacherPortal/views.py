from django.shortcuts import render
from FrontEndAPI.serializers import StudentSerializer
from sap.models import Student
import requests


api_url = "http://127.0.0.1:8000/api"
token = 'Token b003b5015c62f34462cdeb33c419380cd2cc9faa'


def index(req):
    get_students = requests.get(api_url + '/Students', headers={'Authorization': token})
    students = get_students.json()
    return render(req, 'teacherportal/index.html', {'students': students})

