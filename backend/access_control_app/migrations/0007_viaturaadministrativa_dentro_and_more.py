# Generated by Django 5.1.3 on 2024-11-21 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access_control_app', '0006_alter_militar_foto_alter_visitante_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='viaturaadministrativa',
            name='dentro',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='viaturaadministrativa',
            name='qr_code',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='viaturaoperacional',
            name='dentro',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='viaturaoperacional',
            name='qr_code',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]
