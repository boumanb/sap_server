from django.apps import apps
from django_seed import Seed
from django.core.management.base import BaseCommand
from sap.models import *


def seed():
    seeder = Seed.seeder()

    models = apps.get_app_config('sap').get_models()

    for e in models:
        seeder.add_entity(e, 20)

    inserted_pks = seeder.execute()


class Command(BaseCommand):
    def handle(self, **options):
        seed()
