# Generated by Django 5.0.6 on 2025-03-01 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_request_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='requesttype',
            name='identification_number',
            field=models.IntegerField(default=1, unique=True),
            preserve_default=False,
        ),
    ]
