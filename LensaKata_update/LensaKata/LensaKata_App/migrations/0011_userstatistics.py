# Generated by Django 4.2.16 on 2024-12-10 13:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('LensaKata_App', '0010_story_delete_customer_delete_member'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_points', models.IntegerField(default=0)),
                ('completed_challenges', models.IntegerField(default=0)),
                ('new_words_learned', models.IntegerField(default=0)),
                ('last_session_points', models.IntegerField(default=0)),
                ('xp', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
