# Generated by Django 4.2.5 on 2023-09-21 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_alter_investments_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='investments',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
