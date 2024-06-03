# Generated by Django 5.0.6 on 2024-06-02 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0005_alter_payment_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='daily_spending_limit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='user',
            name='total_money',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]