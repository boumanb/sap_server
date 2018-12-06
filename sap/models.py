from django.db import models
from django.utils import timezone


class Device(models.Model):
    installation_uid = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Student(models.Model):
    name = models.CharField(max_length=200)
    card_uid = models.IntegerField()
    email = models.CharField(max_length=200, null=True)
    device = models.OneToOneField(
        Device,
        on_delete=models.CASCADE
    )
    api_token = models.CharField(max_length=200, null=True)
    api_token_valid_till = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def attend(self):
        # Marks attendace for the student. The booleans default to False.
        att = Attendance(student=self)
        att.save()
        
        
    def check_token_valid(self):
        if self.api_token_valid_till > timezone.now():
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
        att = Attendance(student=student, phone_check=True, card_check=True)


class Course(models.Model):
    name = models.CharField(max_length=200)
    teacher = models.ManyToManyField(Teacher)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attendees = models.ManyToManyField(Student)

    def make_collages(self, room, dates, ):

        #Generates the collages tables.
        return 0


class Room(models.Model):
    name = models.CharField(max_length=200)
    reader_UID = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Collage(models.Model):
    day = models.DateField()
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Attendance(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    phone_check = models.BooleanField(default=False)
    card_check = models.BooleanField(default=False)
    phone = models.BooleanField(default=False)
    card = models.BooleanField(default=False)

