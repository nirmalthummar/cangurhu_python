# Generated by Django 3.2.13 on 2022-05-27 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='verificationdevice',
            name='otp',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]