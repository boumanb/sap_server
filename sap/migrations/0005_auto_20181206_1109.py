# Generated by Django 2.1.3 on 2018-12-06 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sap', '0004_auto_20181206_1020'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='installation_UID',
            new_name='installation_uid',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='card_UID',
            new_name='card_uid',
        ),
    ]
