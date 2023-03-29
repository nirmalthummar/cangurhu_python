# Generated by Django 3.2.13 on 2022-09-27 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_storetoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storetoken',
            name='device_type',
            field=models.CharField(blank=True, choices=[('0', 'Android'), ('1', 'iOS'), ('2', 'Windows'), ('3', 'MacOS')], max_length=255, null=True),
        ),
    ]
