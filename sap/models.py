from random import randint
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


class Student(models.Model):
    name = models.CharField(max_length=200)
    student_nr = models.CharField(max_length=200, null=True)
    register_device_digits = models.CharField(max_length=6, null=True)
    register_device_digits_valid_till = models.DateTimeField(null=True)
    card_uid = models.IntegerField()
    email = models.CharField(max_length=200, null=True)
    device = models.OneToOneField(
        Device,
        on_delete=models.CASCADE,
        null=True
    )
    api_token = models.CharField(max_length=200, null=True)
    api_token_valid_till = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def attend(self):
        # Marks attendance for the student. The booleans default to False.
        att = Attendance(student=self)
        att.save()

    def check_token_valid(self):
        if self.api_token_valid_till > timezone.now():
            return True
        else:
            return False

    def verify_registration(self, sent_register_digits):
        if self.register_device_digits_valid_till > timezone.now():
            return "Registration time expired"
        if self.register_device_digits == sent_register_digits:
            self.device.confirmed = True
            self.device.save()
            return True

    def send_registration_mail(self, installation_uid):
        if self.has_confirmed_device():
            return False
        register_digits = randint(100000, 999999)
        self.register_device_digits = register_digits
        self.register_device_digits_valid_till = timezone.now()
        device = Device(installation_uid=installation_uid)
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
        if self.device.is_confirmed():
            return True
        else:
            return False


class Teacher(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def attend_student(self, student):
        Attendance(student=student, phone_check=True, card_check=True)


class Course(models.Model):
    name = models.CharField(max_length=200)
    teacher = models.ManyToManyField(Teacher)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attendees = models.ManyToManyField(Student)

    def make_colleges(self, room, times, dates):
        # Times is a list of tuples(weekday, starttime, endtime)
        # Dates is tuple of (startdate, enddate)
        for e in times:
            weekday = eval("rrule." + e[0])
            days = rrule.rrule(rrule.DAILY,
                               byweekday=weekday,
                               dtstart=dates[0],
                               until=dates[1])

            for x in days:
                coll = Collage(
                    day=x,
                    begin_time=e[1],
                    end_time=e[2],
                    room=room,
                    course=self
                )
                coll.save()


class Room(models.Model):
    name = models.CharField(max_length=200)
    reader_UID = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Collage(models.Model):
    day = models.DateField(null=True)
    begin_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Attendance(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    phone_check = models.BooleanField(default=False)
    card_check = models.BooleanField(default=False)
    phone = models.BooleanField(default=False)
    card = models.BooleanField(default=False)
