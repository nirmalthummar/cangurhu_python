# Generated by Django 3.2.13 on 2022-10-14 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='amount_paid',
            field=models.CharField(choices=[('pending', 'Pending'), ('succeeded', 'Succeeded'), ('failed', 'Failed')], default='pending', max_length=25),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PE', 'pending'), ('OP', 'order placed'), ('ACK', 'cook accepted order'), ('CCK', 'cook canceled order'), ('ACR', 'courier accepted order'), ('CCR', 'courier canceled order'), ('CCU', 'customer canceled order'), ('RCK', 'ready to cook'), ('CP', 'cooking in progress'), ('RE', 'ready'), ('PIU', 'pickedup'), ('OTW', 'on the way'), ('DE', 'delivered')], default='pending', max_length=25),
        ),
    ]
