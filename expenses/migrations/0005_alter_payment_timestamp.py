# Generated by Django 5.0.6 on 2024-06-01 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0004_alter_payment_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
