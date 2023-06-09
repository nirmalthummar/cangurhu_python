# Generated by Django 3.2.13 on 2022-09-12 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0002_marketingfeerate'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryFeesPaidByCook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost_per_mile', models.IntegerField()),
                ('country', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'table_deliveryfeespaidbycook',
            },
        ),
    ]
