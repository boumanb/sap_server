from django.db import models


class Device(models.Model):
    installation_UID = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=200)
    card_UID = models.IntegerField()
    email = models.CharField(max_length=200)
    device = models.OneToOneField(
        Device,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Class(models.Model):
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    room = models.ForeignKey(Room)
    course = models.ForeignKey(Course)

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=200)
    reader_UID = models.CharField(max_length=200)

    def __str__(self):
        return self.name, reader_UID


class Course(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    teacher = models.ForeignKey(Teacher)

    def __str__(self):
        return self.name


class Teacher (models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name, self.email
