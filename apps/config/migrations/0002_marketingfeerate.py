# Generated by Django 3.2.13 on 2022-09-12 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketingFeeRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100)),
                ('percentage', models.IntegerField()),
            ],
            options={
                'db_table': 'table_marketingfeerate',
            },
        ),
    ]
