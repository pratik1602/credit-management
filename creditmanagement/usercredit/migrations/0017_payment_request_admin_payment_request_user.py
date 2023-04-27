# Generated by Django 4.1.4 on 2023-04-27 04:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usercredit', '0016_payment_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment_request',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_admin_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='payment_request',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_user_id', to=settings.AUTH_USER_MODEL),
        ),
    ]