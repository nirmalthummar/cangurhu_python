# Generated by Django 3.2.13 on 2022-09-23 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0021_auto_20220923_0556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cookgradeexplaination',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cookgradeexplaination',
            name='grade',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
    ]