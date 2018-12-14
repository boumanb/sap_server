import datetime
import json

from django.test import TestCase
from django.utils import timezone

from sap.models import Student, Device


class StudentModelTests(TestCase):

    def test_has_device_but_not_confirmed(self):
        student = Student()
        device = Device()
        student.device = device
        self.assertIs(student.has_confirmed_device(), False)

    def test_has_device_confirmed(self):
        student = Student()
        device = Device()
        device.confirmed = True
        student.device = device
        self.assertIs(student.has_confirmed_device(), True)

    def test_init_registration_with_device_confirmed(self):
        student = Student()
        device = Device()
        device.confirmed = True
        student.device = device
        self.assertIs(student.send_registration_mail(installation_uid="test"), False)


class RPCAPITests(TestCase):
    url = "http://127.0.0.1:8000/rpc/"

    @classmethod
    def setUpTestData(cls):
        cls.device = Device.objects.create(installation_uid='123', confirmed=True)
        cls.student = Student.objects.create(
            name='test',
            card_uid='1234',
            student_nr='1234',
            device=cls.device
        )

    def test_echo(self):
        payload = {
            "method": "echo",
            "params": ["echome!"],
            "jsonrpc": "2.0",
            "id": 0,
        }

        response = self.client.post(self.url, data=payload, content_type='application/json')
        jsonresponse = json.loads(response.content)

        assert jsonresponse['result'] == 'echome!'
        assert jsonresponse['jsonrpc']
        assert jsonresponse['id'] == 0

    def test_echo_auth_valid(self):
        payload = {
            "method": "login",
            "params": ["123"],
            "jsonrpc": "2.0",
            "id": 0,
        }

        response = self.client.post(self.url, data=payload, content_type='application/json')
        jsonresponse = json.loads(response.content)

        self.student.refresh_from_db()

        assert jsonresponse['result']['valid_till']
        assert jsonresponse['result']['token']
        assert jsonresponse['jsonrpc']
        assert jsonresponse['id'] == 0
        assert jsonresponse['result']['token'] == self.student.api_token

        payload = {
            "method": "echo_with_auth",
            "params": ["echome!"],
            "jsonrpc": "2.0",
            "id": 1,
        }

        response = self.client.post(self.url, data=payload, content_type='application/json', **{"HTTP_AUTHORIZATION": jsonresponse['result']['token']})
        jsonresponse = json.loads(response.content)

        assert jsonresponse['result'] == 'echome!'
        assert jsonresponse['jsonrpc']
        assert jsonresponse['id'] == 1

    def test_echo_auth_expired(self):
        payload = {
            "method": "login",
            "params": ["123"],
            "jsonrpc": "2.0",
            "id": 0,
        }

        response = self.client.post(self.url, data=payload, content_type='application/json')
        jsonresponse = json.loads(response.content)

        self.student.refresh_from_db()
        self.student.api_token_valid_till = timezone.now() + datetime.timedelta(minutes=-10)
        self.student.save()

        assert jsonresponse['result']['valid_till']
        assert jsonresponse['result']['token']
        assert jsonresponse['jsonrpc']
        assert jsonresponse['id'] == 0
        assert jsonresponse['result']['token'] == self.student.api_token

        payload = {
            "method": "echo_with_auth",
            "params": ["echome!"],
            "jsonrpc": "2.0",
            "id": 1,
        }

        response = self.client.post(self.url, data=payload, content_type='application/json',
                                    **{"HTTP_AUTHORIZATION": jsonresponse['result']['token']})
        jsonresponse = json.loads(response.content)

        assert jsonresponse['error']['code'] == -32603
        self.assertIn('Authentication failed when calling', jsonresponse['error']['message'])
        self.assertEqual(response.status_code, 403)
        assert jsonresponse['id'] == 1

    def test_login(self):
        payload = {
            "method": "login",
            "params": ["123"],
            "jsonrpc": "2.0",
            "id": 0,
        }

        response = self.client.post(self.url, data=payload, content_type='application/json')
        jsonresponse = json.loads(response.content)

        self.student.refresh_from_db()

        assert jsonresponse['result']['valid_till']
        assert jsonresponse['result']['token']
        assert jsonresponse['jsonrpc']
        assert jsonresponse['id'] == 0
        assert jsonresponse['result']['token'] == self.student.api_token
