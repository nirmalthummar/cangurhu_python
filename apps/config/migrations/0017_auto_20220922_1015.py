# Generated by Django 3.2.13 on 2022-09-22 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0016_auto_20220922_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payoutrateandconstant',
            name='banking_payout_constant',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
        migrations.AlterField(
            model_name='payoutrateandconstant',
            name='banking_payout_fee',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
    ]