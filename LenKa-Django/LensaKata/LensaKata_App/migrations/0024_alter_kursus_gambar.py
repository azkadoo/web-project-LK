# Generated by Django 4.2.16 on 2024-12-14 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LensaKata_App', '0023_kursus_videodetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kursus',
            name='gambar',
            field=models.ImageField(blank=True, null=True, upload_to='kursus_images/'),
        ),
    ]