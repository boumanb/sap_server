# Generated by Django 2.1.3 on 2018-12-14 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sap', '0015_auto_20181213_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='device',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sap.Device'),
        ),
    ]