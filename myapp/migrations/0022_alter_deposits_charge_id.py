# Generated by Django 4.2.5 on 2023-10-03 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0021_deposits_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposits',
            name='charge_id',
            field=models.CharField(default='', max_length=100),
        ),
    ]