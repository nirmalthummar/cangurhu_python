# Generated by Django 3.2.12 on 2022-10-17 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_cartmenuitem_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartmenuitem',
            name='order_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]