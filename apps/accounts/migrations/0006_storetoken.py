# Generated by Django 3.2.13 on 2022-09-26 06:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_delete_verificationdevice'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('device_type', models.CharField(blank=True, choices=[(0, 'Android'), (1, 'iOS'), (2, 'Windows'), (3, 'MacOS')], max_length=255, null=True)),
                ('device_token', models.CharField(blank=True, max_length=255, null=True)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'table_store_token',
            },
        ),
    ]
