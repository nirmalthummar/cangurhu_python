# Generated by Django 3.2.13 on 2022-06-02 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={},
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AlterModelTable(
            name='customer',
            table='table_customer',
        ),
    ]
