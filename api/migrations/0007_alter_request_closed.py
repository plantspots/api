# Generated by Django 5.0.6 on 2025-03-01 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_request_email_contact_request_phone_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='closed',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
