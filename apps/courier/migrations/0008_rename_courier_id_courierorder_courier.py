# Generated by Django 3.2.13 on 2022-08-31 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courier', '0007_alter_courierorder_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courierorder',
            old_name='courier_id',
            new_name='courier',
        ),
    ]
