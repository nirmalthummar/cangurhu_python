# Generated by Django 3.2.13 on 2022-09-06 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PE', 'Pending'), ('OP', 'Order placed'), ('ACK', 'Cook Accepted Order'), ('CCK', 'Cook Canceled Order'), ('ACR', 'Courier Accepted Order'), ('CCR', 'Courier Canceled Order'), ('RCK', 'Ready To Cook'), ('CP', 'Cooking In Progress'), ('RE', 'Ready'), ('PI', 'Pickup'), ('OTW', 'on the way'), ('DE', 'delivered')], default='PE', max_length=25),
        ),
    ]