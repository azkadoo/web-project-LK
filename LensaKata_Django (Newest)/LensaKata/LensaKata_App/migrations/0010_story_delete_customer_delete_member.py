# Generated by Django 4.2.16 on 2024-11-21 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LensaKata_App', '0009_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('question', models.CharField(max_length=300)),
                ('answer', models.TextField(help_text='Pisahkan jawaban dengan koma, contoh: bidadari,telaga,Jaka Tarub')),
                ('tags', models.TextField(help_text='Pisahkan tag dengan koma, contoh: langit,menangis,telaga')),
            ],
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Member',
        ),
    ]