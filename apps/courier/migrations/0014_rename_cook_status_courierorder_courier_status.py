# Generated by Django 3.2.13 on 2022-09-16 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courier', '0013_alter_courierorder_cook_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courierorder',
            old_name='cook_status',
            new_name='courier_status',
        ),
    ]
