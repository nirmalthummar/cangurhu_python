# Generated by Django 3.2.13 on 2022-09-29 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='is_ready',
            new_name='is_read',
        ),
    ]
