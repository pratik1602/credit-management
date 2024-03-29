# Generated by Django 4.1.4 on 2023-04-27 06:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usercredit', '0018_rename_created_at_payment_request_requested_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='card_status',
        ),
        migrations.RemoveField(
            model_name='card',
            name='payment_method',
        ),
        migrations.AddField(
            model_name='payment_request',
            name='payment_method',
            field=models.CharField(default='Cycle', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment_request',
            name='payment_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transaction',
            name='commission',
            field=models.FloatField(blank=True, default=2.0, null=True, validators=[django.core.validators.MinValueValidator(0.9), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
