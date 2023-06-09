# Generated by Django 3.2.12 on 2022-10-18 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cook', '0021_auto_20220916_1540'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cookorderdetails',
            options={},
        ),
        migrations.AddField(
            model_name='cookorderdetails',
            name='is_future_order',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cookorderdetails',
            name='order_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterModelTable(
            name='cookorderdetails',
            table='table_cook_order_details',
        ),
    ]
