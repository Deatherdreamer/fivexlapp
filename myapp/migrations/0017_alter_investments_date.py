# Generated by Django 4.2.5 on 2023-09-21 13:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_alter_profile_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investments',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
