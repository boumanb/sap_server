# Generated by Django 2.1.3 on 2018-12-14 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sap', '0016_auto_20181214_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='installation_uid',
            field=models.BinaryField(unique=True),
        ),
    ]