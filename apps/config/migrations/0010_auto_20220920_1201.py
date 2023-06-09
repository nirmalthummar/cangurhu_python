# Generated by Django 3.2.13 on 2022-09-20 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0009_auto_20220920_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='constantpay',
            name='high_value',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
        migrations.AlterField(
            model_name='constantpay',
            name='low_value',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
        migrations.AlterField(
            model_name='constantpay',
            name='medium_value',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
    ]
