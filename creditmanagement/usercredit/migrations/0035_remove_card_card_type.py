# Generated by Django 4.1.4 on 2023-05-10 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usercredit', '0034_remove_card_card_photo_card_backside_card_photo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='card_type',
        ),
    ]
