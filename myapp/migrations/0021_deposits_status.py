# Generated by Django 4.2.5 on 2023-09-27 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_tasks_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='deposits',
            name='status',
            field=models.CharField(default='pending', max_length=100),
        ),
    ]
