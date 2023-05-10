# Generated by Django 4.1.4 on 2023-05-09 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usercredit', '0033_alter_transaction_payment_method_flag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='card_photo',
        ),
        migrations.AddField(
            model_name='card',
            name='backside_card_photo',
            field=models.ImageField(default='', upload_to='Images\\Cards\\BackSide'),
        ),
        migrations.AddField(
            model_name='card',
            name='frontside_card_photo',
            field=models.ImageField(default='', upload_to='Images\\Cards\\FrontSide'),
        ),
    ]