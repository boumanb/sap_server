from django.test import TestCase

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
