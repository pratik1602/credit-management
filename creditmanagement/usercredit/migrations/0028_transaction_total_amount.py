# Generated by Django 4.1.4 on 2023-05-05 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usercredit', '0027_rename_charges_transaction_deposit_charges_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='total_amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
