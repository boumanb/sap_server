from django.apps import apps
from django_seed import Seed
from django.core.management.base import BaseCommand
from sap.models import *
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



class Command(BaseCommand):
    def handle(self, **options):
        seed()
