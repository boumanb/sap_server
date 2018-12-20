import datetime
import json

from django.test import TestCase
from django.utils import timezone

from sap.models import Student, Device, Room, Course, Teacher, Attendance


class StudentModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.device = Device.objects.create(installation_uid='123', confirmed=True)
        cls.student = Student.objects.create(
            name='test',
            card_uid='1234',
            student_nr='1234',
            device=cls.device
        )
        cls.room = Room.objects.create(name='Test', reader_UID='12345')
        cls.teacher = Teacher.objects.create(name='Test teacher', password='test', email='test@test.nl')

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
        cls.room = Room.objects.create(name='Test', reader_UID='12345')
        cls.teacher = Teacher.objects.create(name='Test teacher', password='test', email='test@test.nl')
        cls.course = Course.objects.create(name='Computer science')
        cls.course.teacher.add(cls.teacher)
        cls.course.attendees.add(cls.student)
        now = timezone.now()
        now_plus_10_min = now + datetime.timedelta(minutes=10)
        d1 = datetime.date(year=now.year, month=now.month, day=1)
        d2 = datetime.date(year=now.year, month=now.month, day=31)
        t1 = datetime.time(hour=now.hour, minute=now.minute)
        t2 = datetime.time(hour=now_plus_10_min.hour, minute=now_plus_10_min.minute)
        day_str = now.strftime('%a')[:2].upper()
        dates = (d1, d2)
        cls.course.make_colleges(cls.room, [(day_str, t1, t2)], dates)

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

        response = self.client.post(self.url, data=payload, content_type='application/json',
                                    **{"HTTP_AUTHORIZATION": jsonresponse['result']['token']})
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

    def test_login_success(self):
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

    def test_login_fail_no_device(self):
        payload = {
            "method": "login",
            "params": ["1234"],
            "jsonrpc": "2.0",
            "id": 0,
        }

        response = self.client.post(self.url, data=payload, content_type='application/json')
        jsonresponse = json.loads(response.content)

        self.student.refresh_from_db()

        self.assertEqual(jsonresponse['result']['success'], False)
        assert jsonresponse['jsonrpc']
        assert jsonresponse['id'] == 0
        assert jsonresponse['result']['msg'] == 'no device found'

    def test_login_fail_no_device_confirmation(self):
        payload = {
            "method": "login",
            "params": ["123"],
            "jsonrpc": "2.0",
            "id": 0,
        }

        self.student.device.confirmed = False
        self.student.device.save()

        response = self.client.post(self.url, data=payload, content_type='application/json')
        jsonresponse = json.loads(response.content)

        self.student.refresh_from_db()

        self.assertEqual(jsonresponse['result']['success'], False)
        assert jsonresponse['jsonrpc']
        assert jsonresponse['id'] == 0
        assert jsonresponse['result']['msg'] == 'device not confirmed'

    def test_attend_card_success(self):
        payload = {
            "method": "card_check",
            "params": ["1234", "12345"],
            "jsonrpc": "2.0",
            "id": 0,
        }

        response = self.client.post(self.url, data=payload, content_type='application/json')
        jsonresponse = json.loads(response.content)
        self.assertEqual(jsonresponse['result']['success'], True)
        attendances = self.student.get_attendances()
        self.assertEqual(attendances.count(), 1)
        self.assertEqual(attendances[0].card_check, True)

    def test_attend_phone_success(self):
        payload = {
            "method": "card_check",
            "params": ["1234", "12345"],
            "jsonrpc": "2.0",
            "id": 0,
        }

        self.client.post(self.url, data=payload, content_type='application/json')

        payload = {
            "method": "phone_check",
            "params": ["123"],
            "jsonrpc": "2.0",
            "id": 0,
        }

        response = self.client.post(self.url, data=payload, content_type='application/json')
        jsonresponse = json.loads(response.content)
        self.assertEqual(jsonresponse['result']['success'], True)
        self.assertEqual(jsonresponse['result']['msg'], 'attendance marked')
        attendances = self.student.get_attendances()
        self.assertEqual(attendances.count(), 1)
        self.assertEqual(attendances[0].card_check, True)
        self.assertEqual(attendances[0].phone_check, True)

    def test_attend_phone_fail_no_card(self):
        payload = {
            "method": "phone_check",
            "params": ["123"],
            "jsonrpc": "2.0",
            "id": 0,
        }

        response = self.client.post(self.url, data=payload, content_type='application/json')
        jsonresponse = json.loads(response.content)
        self.assertEqual(jsonresponse['result']['success'], False)
        self.assertEqual(jsonresponse['result']['msg'], 'try again')
        attendances = self.student.get_attendances()
        self.assertEqual(attendances.count(), 0)

    def test_attend_phone_fail_too_slow(self):
        payload = {
            "method": "card_check",
            "params": ["1234", "12345"],
            "jsonrpc": "2.0",
            "id": 0,
        }

        self.client.post(self.url, data=payload, content_type='application/json')

        attendances = self.student.get_attendances()
        self.assertEqual(attendances.count(), 1)
        attendance = attendances[0]
        self.assertEqual(attendance.card_check, True)
        attendance.timestamp = attendance.timestamp - datetime.timedelta(seconds=10)
        attendance.save()

        payload = {
            "method": "phone_check",
            "params": ["123"],
            "jsonrpc": "2.0",
            "id": 0,
        }

        response = self.client.post(self.url, data=payload, content_type='application/json')

        jsonresponse = json.loads(response.content)
        self.assertEqual(jsonresponse['result']['success'], False)
        self.assertEqual(jsonresponse['result']['msg'], 'try again')
        self.assertEqual(attendances.count(), 1)
        self.assertEqual(attendances[0].card_check, True)
        self.assertEqual(attendances[0].phone_check, False)

