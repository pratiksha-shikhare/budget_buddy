# Generated by Django 5.0.6 on 2024-06-04 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0010_payment_remain_daily_target_amt'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='cash_payment',
            field=models.BooleanField(default=False),
        ),
    ]
