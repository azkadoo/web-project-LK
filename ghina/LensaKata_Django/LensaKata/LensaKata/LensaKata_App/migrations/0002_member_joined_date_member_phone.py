# Generated by Django 5.1.2 on 2024-11-05 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LensaKata_App', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='joined_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='phone',
            field=models.IntegerField(null=True),
        ),
    ]
