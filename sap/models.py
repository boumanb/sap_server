from datetime import date
from random import randint

import bcrypt
from dateutil import rrule
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone


class Device(models.Model):
    installation_uid = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed = models.BooleanField(default=False)

    def is_confirmed(self):
        if self.confirmed is True:
            return True
        else:
            return False

    def confirm_device(self):
        self.confirmed = True
        self.save()

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Student(models.Model):
    name = models.CharField(max_length=200)
    student_nr = models.CharField(max_length=200, null=True)
    register_device_digits = models.CharField(max_length=6, null=True)
    register_device_digits_valid_till = models.DateTimeField(null=True)
    card_uid = models.IntegerField()
    email = models.CharField(max_length=200, null=True)
    device = models.OneToOneField(
        Device,
        on_delete=models.SET_NULL,
        null=True
    )
    api_token = models.CharField(max_length=200, null=True)
    api_token_valid_till = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def attend_card(self, college):
        # Marks attendance for the student. The booleans default to False.
        att = Attendance(student=self, college=college, card_check=True)
        att.save()

    def check_token_valid(self):
        if self.api_token_valid_till > timezone.now():
            return True
        else:
            return False

    def verify_registration(self, sent_register_digits, installation_uid):
        if self.register_device_digits_valid_till > timezone.now():
            return "Registration time expired"
        if self.register_device_digits == sent_register_digits and bcrypt.checkpw(installation_uid.encode('utf-8'), self.device.installation_uid.encode('utf-8')):
            self.device.confirmed = True
            self.device.save()
            return True

    def verify_device_installation_uid(self, installation_uid):
        if bcrypt.checkpw(installation_uid.encode('utf-8'), self.device.installation_uid.encode('utf-8')):
            return True
        else:
            return False

    def send_registration_mail(self, installation_uid):
        if self.has_confirmed_device():
            return False
        register_digits = randint(100000, 999999)
        self.register_device_digits = register_digits
        self.register_device_digits_valid_till = timezone.now()
        salt = bcrypt.gensalt()
        hashed_installation_uid = bcrypt.hashpw(installation_uid.encode('utf-8'), salt)
        device = Device(installation_uid=hashed_installation_uid.decode('utf-8'))
        device.save()
        self.device = device
        self.save()
        send_mail(
            'Confirm device registration',
            'Here is the message.'
            '\n'
            'Registration code: ' + str(register_digits) + '',
            'nsasapattendance@gmail.com',
            [self.email],
            fail_silently=False,
        )
        return True

    def has_confirmed_device(self):
        if self.device and self.device.is_confirmed():
            return True
        else:
            return False

    def get_attendances(self):
        attendances = Attendance.objects.filter(student=self)
        return attendances

    @staticmethod
    def get_by_apitoken(api_token):
        student_qs = Student.objects.filter(api_token=api_token)
        if not student_qs:
            return None
        else:
            return student_qs[0]

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Teacher(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def attend_student(self, student, college):
        Attendance(student=student, college=college, phone_check=True, card_check=True)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Course(models.Model):
    name = models.CharField(max_length=200)
    teacher = models.ManyToManyField(Teacher)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attendees = models.ManyToManyField(Student)

    def make_colleges(self, room, times, dates):
        # Times is a list of tuples(weekday, starttime, endtime)
        # Dates is tuple of (startdate, enddate)

        options = {"MO": rrule.MO,
                   "TU": rrule.TU,
                   "WE": rrule.WE,
                   "TH": rrule.TH,
                   "FR": rrule.FR,
                   "SA": rrule.SA,
                   "SU": rrule.SU,
                   }

        for e in times:
            weekday = options[e[0]]
            days = rrule.rrule(rrule.DAILY,
                               byweekday=weekday,
                               dtstart=dates[0],
                               until=dates[1])

            for x in days:
                coll = College(
                    day=x,
                    begin_time=e[1],
                    end_time=e[2],
                    room=room,
                    course=self
                )
                coll.save()

    def get_colleges(self):
        return College.objects.filter(course=self)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


# noinspection PyMethodMayBeStatic
class Room(models.Model):
    name = models.CharField(max_length=200)
    reader_UID = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def find_college(self):
        # Returns the current college held in the room
        college = College.objects.get(
            day=date.today(),
            begin_time__lte=timezone.now(),
            end_time__gte=timezone.now())

        return college

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class College(models.Model):
    day = models.DateField(null=True)
    begin_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Attendance(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE, unique=False, null=True)
    phone_check = models.BooleanField(default=False)
    card_check = models.BooleanField(default=False)
    phone = models.BooleanField(default=False)
    card = models.BooleanField(default=False)

    def attend_phone(self):
        self.phone_check = True
        self.save()

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
