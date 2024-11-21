# Generated by Django 5.1.3 on 2024-11-21 03:01

import access_control_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access_control_app', '0004_registroacesso_viatura_administrativa_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='militar',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to=access_control_app.models.upload_to),
        ),
        migrations.AddField(
            model_name='visitante',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to=access_control_app.models.upload_to),
        ),
    ]