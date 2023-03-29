# Generated by Django 3.2.13 on 2022-10-10 04:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0002_country_flag'),
        ('accounts', '0008_stripecustomeruser'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bank_name', models.CharField(blank=True, max_length=255, null=True)),
                ('account_no', models.CharField(blank=True, max_length=30, null=True)),
                ('account_holder_name', models.CharField(blank=True, max_length=255, null=True)),
                ('bank_ifsc_code', models.CharField(blank=True, max_length=20, null=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snippets.country')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'abstract': False,
            },
        ),
    ]