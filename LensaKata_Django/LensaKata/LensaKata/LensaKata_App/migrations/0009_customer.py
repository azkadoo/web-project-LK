# Generated by Django 4.2.16 on 2024-11-08 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LensaKata_App', '0008_delete_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]