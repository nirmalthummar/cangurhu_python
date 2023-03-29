# Generated by Django 3.2.13 on 2022-08-31 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_alter_order_tip_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('order placed', 'Order placed'), ('accepted', 'Accepted'), ('canceled', 'Canceled'), ('on the way', 'on the way'), ('delivered', 'delivered')], default='pending', max_length=15),
        ),
    ]