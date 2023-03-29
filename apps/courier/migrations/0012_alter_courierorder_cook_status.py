# Generated by Django 3.2.13 on 2022-09-08 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courier', '0011_courierorder_cook_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courierorder',
            name='cook_status',
            field=models.CharField(choices=[('PE', 'pending'), ('PIU', 'picked up'), ('OTW', 'on the way'), ('DE', 'delivered'), ('ACR', 'courier accepted order'), ('CCR', 'courier canceled order')], default='PE', max_length=25),
        ),
    ]
