# Generated by Django 3.2.13 on 2022-08-31 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_order_amount_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='tip_type',
            field=models.CharField(choices=[('none', 'None'), ('percentage', 'Percentage'), ('amount', 'Amount')], default='none', max_length=11),
        ),
    ]