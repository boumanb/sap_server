# Generated by Django 2.1.3 on 2018-12-12 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sap', '0010_auto_20181207_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collage',
            name='begin_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='collage',
            name='end_time',
            field=models.TimeField(null=True),
        ),
    ]
