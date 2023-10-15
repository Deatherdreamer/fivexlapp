# Generated by Django 4.2.4 on 2023-09-03 02:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_profile_referred_by_alter_profile_referral_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='name',
            new_name='firstName',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='phone',
            new_name='lastName',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='date',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='desc',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
        migrations.AddField(
            model_name='profile',
            name='dateJoined',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='dateOfBirth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
