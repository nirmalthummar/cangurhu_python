# Generated by Django 3.2.13 on 2022-06-07 15:50

import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courier', '0003_auto_20220602_1001'),
    ]

    operations = [
        migrations.AddField(
            model_name='courier',
            name='contract_signature',
            field=models.FileField(blank=True, null=True, upload_to=core.utils.upload_path_handler),
        ),
        migrations.AddField(
            model_name='courier',
            name='driving_licence',
            field=models.FileField(blank=True, null=True, upload_to=core.utils.upload_path_handler),
        ),
        migrations.AddField(
            model_name='courier',
            name='e_signed_contract',
            field=models.FileField(blank=True, null=True, upload_to=core.utils.upload_path_handler),
        ),
        migrations.AddField(
            model_name='courier',
            name='govt_cert',
            field=models.FileField(blank=True, null=True, upload_to=core.utils.upload_path_handler),
        ),
        migrations.AddField(
            model_name='courier',
            name='vehicle_insurance',
            field=models.FileField(blank=True, null=True, upload_to=core.utils.upload_path_handler),
        ),
        migrations.AddField(
            model_name='courier',
            name='vehicle_registration',
            field=models.FileField(blank=True, null=True, upload_to=core.utils.upload_path_handler),
        ),
        migrations.AddField(
            model_name='courier',
            name='vehicle_type',
            field=models.CharField(blank=True, choices=[('motorbike', 'Motorbike'), ('bike', 'Bike'), ('by_foot', 'By Foot')], max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='courier',
            name='work_permit',
            field=models.FileField(blank=True, null=True, upload_to=core.utils.upload_path_handler),
        ),
    ]