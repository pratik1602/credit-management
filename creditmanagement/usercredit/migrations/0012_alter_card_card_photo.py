# Generated by Django 4.1.4 on 2023-04-20 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usercredit', '0011_alter_transaction_due_paid_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_photo',
            field=models.ImageField(default='', upload_to='Images\\Card'),
        ),
    ]
