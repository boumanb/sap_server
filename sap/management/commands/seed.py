from django.apps import apps
from django_seed import Seed
from django.core.management.base import BaseCommand
from sap.models import *
import datetime
import random
import pyotp

seeder = Seed.seeder()

def generateDeviceStudent():
    d = Device(
        installation_uid=seeder.faker.ean13()
    )
    d.save()
    s = Student(
        name=seeder.faker.ean13(),
        card_uid=random.randint(1000000, 9999999),
        email=seeder.faker.email(),
        device=d
        )
    s.save()

def populateCourse():
    course = Course.objects.get(id=1)
    teacher = Teacher.objects.get(id=1)

    course.teacher.add(teacher)
    students = Student.objects.all()[:5]

    for e in students:
        course.attendees.add(e)


def generateCollages():
    course = Course.objects.get(id=1)
    room = Room.objects.get(id=1)

    d1 = seeder.faker.date_between(start_date='today', end_date='+1w')
    d2 = seeder.faker.date_between(start_date='today', end_date='+6m')

    t1 = seeder.faker.time
    t2 = datetime.time(hour=14, minute=30)

    t3 = seeder.faker.time
    t4 = datetime.time(hour=16, minute=30)


    time = [("MO", t1, t2), ("TU", t2, t3)]
    date = (d1, d2)

    course.make_colleges(room, time, date)

def seed():


    for e in range (10):
        generateDeviceStudent()

    for e in range(10):
        s = Student(
            name=seeder.faker.ean13(),
            card_uid=random.randint(1000000, 9999999),
            email=seeder.faker.email(),
        )
        s.save()

    seeder.add_entity(Room, 10, {
        'name': lambda x: seeder.faker.street_suffix(),
        'reader_UID': lambda x: seeder.faker.ean13()
    })

    seeder.add_entity(Teacher, 5, {
        'name': lambda x: seeder.faker.name(),
        'password': lambda x: seeder.faker.password(),
        'email': lambda x: seeder.faker.email()
    })

    seeder.add_entity(Course, 5, {
        'name': lambda x: seeder.faker.catch_phrase(),
    })
    seeder.execute()
    populateCourse()
    generateCollages()



class Command(BaseCommand):
    def handle(self, **options):
        seed()
