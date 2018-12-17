from django_seed import Seed
from django.core.management.base import BaseCommand
from sap.models import *
import datetime
import random

seeder = Seed.seeder()


def generate_device_student():
    d = Device(
        installation_uid=seeder.faker.ean13()
    )
    d.save()
    s = Student(
        name=seeder.faker.name(),
        card_uid=random.randint(1000000, 9999999),
        email=seeder.faker.email(),
        device=d
    )
    s.save()


def populate_course():
    course = Course.objects.get(id=1)
    teacher = Teacher.objects.get(id=1)

    course.teacher.add(teacher)
    students = Student.objects.all()[:10]

    for e in students:
        course.attendees.add(e)


def generate_colleges():
    course = Course.objects.get(id=1)
    room = Room.objects.get(id=1)

    d1 = datetime.date(year=2018, month=6, day=15)
    d2 = datetime.date(year=2018, month=8, day=15)

    t1 = datetime.time(hour=13, minute=30)
    t2 = datetime.time(hour=14, minute=30)

    t3 = datetime.time(hour=11, minute=30)
    t4 = datetime.time(hour=16, minute=30)

    time = [("MO", t1, t2), ("TU", t3, t4)]
    date = (d1, d2)

    course.make_colleges(room, time, date)


def seed():
    for e in range(10):
        generate_device_student()

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
    populate_course()
    generate_colleges()


class Command(BaseCommand):
    def handle(self, **options):
        seed()
