# Generated by Django 3.2.13 on 2022-09-08 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courier', '0012_alter_courierorder_cook_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courierorder',
            name='cook_status',
            field=models.CharField(choices=[('PE', 'pending'), ('ACR', 'courier accepted order'), ('CCR', 'courier canceled order'), ('PIU', 'picked up'), ('OTW', 'on the way'), ('DE', 'delivered')], default='PE', max_length=25),
        ),
    ]
