# Generated by Django 3.2.13 on 2022-09-01 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0003_translatedata'),
    ]

    operations = [
        migrations.AddField(
            model_name='translatedata',
            name='translated',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]