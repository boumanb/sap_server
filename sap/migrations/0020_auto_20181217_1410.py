# Generated by Django 2.1.3 on 2018-12-17 13:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sap', '0019_auto_20181215_1440'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='attendees',
        ),
        migrations.AddField(
            model_name='collage',
            name='attendees',
            field=models.ManyToManyField(to='sap.Student'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
