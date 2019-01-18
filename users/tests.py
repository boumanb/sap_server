from django.test import TestCase, Client
from django.contrib.auth.models import User
from sap.models import Teacher


class UserTestCase(TestCase):
    url = 'http://127.0.0.1:8000/teacherportal'

    def setUp(self):
        user = User.objects.create(username="bert")
        teacher = Teacher.objects.create(name="Jaap", email="Jaap@hr.nl", user=user)
        user.set_password('@Welkom1')
        user.save()

    def userLogin(self):
        client = Client()
        response = client.login(username='bert', password='@Welkom1')

        self.assertTrue(response)

    def user_login_wrong_credentials(self):
        client = Client()
        response = client.login(username='bert', password='Admin123')

        self.assertFalse(response)

    def teacher_page_logged_in(self):
        client = Client()
        response = client.login(username='bert', password='@Welkom1')
        web = client.get(self.url + '/teacher/')

        assert web.status_code == 200

    def teacher_page_not_logged_in(self):
        client = Client()
        response = client.login(username='bert', password='@@@@@')
        web = client.get(self.url + '/teacher/')

        assert web.status_code == 302
