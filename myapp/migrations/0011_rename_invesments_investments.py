# Generated by Django 4.2.4 on 2023-09-09 01:36

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0010_profile_balance'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Invesments',
            new_name='Investments',
        ),
    ]
