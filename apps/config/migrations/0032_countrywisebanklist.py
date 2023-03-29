# Generated by Django 3.2.13 on 2022-10-07 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0031_auto_20220929_1751'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountryWiseBankList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100)),
                ('bank_name', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'table_countrywise_bank_list',
            },
        ),
    ]
