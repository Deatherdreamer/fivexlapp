# Generated by Django 4.2.4 on 2023-09-03 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_rename_name_profile_firstname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='firstName',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='lastName',
            field=models.CharField(default='', max_length=100),
        ),
    ]