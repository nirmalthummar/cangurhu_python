# Generated by Django 3.2.13 on 2022-08-26 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_order_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
    ]
