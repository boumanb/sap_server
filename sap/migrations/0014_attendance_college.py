# Generated by Django 2.1.3 on 2018-12-13 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sap', '0013_merge_20181213_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='college',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='sap.Collage'),
        ),
    ]
