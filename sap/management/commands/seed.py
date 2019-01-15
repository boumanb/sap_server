from django_seed import Seed
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token

from sap.models import *
import datetime
import random

seeder = Seed.seeder()

NORMAL_STUDENTS_AMOUNT = 10
STUDENTS_WITH_DEVICE_AMOUNT = 10
ROOMS_AMOUNT = 10
TEACHER_AMOUNT = 1
COURSE_AMOUNT = 5


def generate_device_student():
    d = Device(
        installation_uid=seeder.faker.ean13()
    )
    d.save()
    s = Student(
        name=seeder.faker.name(),
        card_uid=random.randint(1000000, 9999999),
        student_nr=random.randint(10000, 999999),
        email=seeder.faker.email(),
        device=d
    )
    s.save()


def populate_course():
    courses = Course.objects.all()[:COURSE_AMOUNT]
    students = Student.objects.all()[:10]
    teacher = Teacher.objects.get(id=1)

    for course in courses:
        course.teacher.add(teacher)
        for s in students:
            course.attendees.add(s)


def generate_colleges(teacher=False):
    course = Course.objects.get(id=1)
    room = Room.objects.get(id=1)

    d1 = datetime.date(year=2019, month=1, day=1)
    d2 = datetime.date(year=2019, month=12, day=30)

    t1 = datetime.time(hour=13, minute=30)
    t2 = datetime.time(hour=14, minute=30)

    t3 = datetime.time(hour=11, minute=30)
    t4 = datetime.time(hour=16, minute=30)

    time = [("MO", t1, t2), ("TU", t3, t4), ("WE", t3, t4), ("TH", t3, t4), ("FR", t3, t4)]
    date = (d1, d2)
    if teacher:
        course.make_colleges(room, time, date, teacher=teacher)
    else:
        course.make_colleges(room, time, date)


def seed(options):
    u_default = User()
    u_default.save()
    t = False
    if options.get('t_username') and options.get('t_password'):
        u = User()
        u.username = options.get('t_username')
        u.set_password(options.get('t_password'))
        u.save()
        Token.objects.create(user=u)
        t = Teacher(user=u, name='SAP test teacher', email='sap_test_teacher@gmail.com')
        t.save()
        print('\nteacher created with given credentials')
        print('Username: %s' % options.get('t_username'))
        print('Password: %s \n' % options.get('t_password'))

    for e in range(STUDENTS_WITH_DEVICE_AMOUNT):
        generate_device_student()
    print(str(STUDENTS_WITH_DEVICE_AMOUNT) + ' device students created')

    for e in range(NORMAL_STUDENTS_AMOUNT):
        s = Student(
            name=seeder.faker.name(),
            card_uid=random.randint(1000000, 9999999),
            student_nr=random.randint(10000, 999999),
            email=seeder.faker.email(),
        )
        s.save()
    print(str(NORMAL_STUDENTS_AMOUNT) + ' normal students created')

    seeder.add_entity(Room, ROOMS_AMOUNT, {
        'name': lambda x: seeder.faker.street_suffix(),
        'reader_UID': lambda x: seeder.faker.ean13()
    })
    print(str(ROOMS_AMOUNT) + ' rooms created')

    seeder.add_entity(Teacher, TEACHER_AMOUNT, {
        'name': lambda x: seeder.faker.name(),
        'email': lambda x: seeder.faker.email(),
        'user': u_default
    })
    print(str(TEACHER_AMOUNT) + ' teachers created')

    seeder.add_entity(Course, COURSE_AMOUNT, {
        'name': lambda x: seeder.faker.catch_phrase(),
    })
    print(str(COURSE_AMOUNT) + ' courses created')

    seeder.execute()
    print('seeder executed')
    populate_course()
    print('course populated')
    generate_colleges(t)
    print('colleges generated')


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--t_username', type=str, help="teacher username")
        parser.add_argument('--t_password', type=str, help="teacher password")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        seed(options)
        self.stdout.write('done seeding')
