# Generated by Django 2.1.3 on 2018-12-06 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sap', '0003_attendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='api_token',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='api_token_valid_till',
            field=models.DateTimeField(null=True),
        ),
    ]