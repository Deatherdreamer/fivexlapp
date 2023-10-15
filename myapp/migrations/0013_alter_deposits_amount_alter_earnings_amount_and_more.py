# Generated by Django 4.2.5 on 2023-09-14 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_earnings_date_earnings_description_earnings_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposits',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='earnings',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='investments',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='investments',
            name='returns',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='withdrawals',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
    ]