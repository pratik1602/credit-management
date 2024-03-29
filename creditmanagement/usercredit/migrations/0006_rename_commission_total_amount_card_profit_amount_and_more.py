# Generated by Django 4.1.4 on 2023-04-14 05:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usercredit', '0005_alter_card_available_balance_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='commission_total_amount',
            new_name='profit_amount',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='amount_paid',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='commission',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='due_paid_through',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='paid_at',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='profit_amount',
        ),
        migrations.AddField(
            model_name='card',
            name='due_paid_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='card',
            name='due_paid_through',
            field=models.CharField(default='Google pay', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='card',
            name='paid_amount',
            field=models.FloatField(default=0),
        ),
    ]
