# Generated by Django 3.2.13 on 2022-09-08 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cook', '0016_merge_20220907_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='cookorderdetails',
            name='cook_status',
            field=models.CharField(choices=[('PE', 'pending'), ('CP', 'cooking in progress'), ('RE', 'ready'), ('REP', 'ready to pickup')], default='PE', max_length=25),
        ),
    ]
