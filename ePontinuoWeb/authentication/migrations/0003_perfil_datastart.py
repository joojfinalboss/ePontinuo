# Generated by Django 5.0.1 on 2024-01-05 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_perfil_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='dataStart',
            field=models.DateField(default=None, null=True),
        ),
    ]
