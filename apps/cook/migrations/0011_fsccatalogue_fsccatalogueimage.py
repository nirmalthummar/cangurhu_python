# Generated by Django 3.2.13 on 2022-07-27 07:49

import core.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cook', '0010_foodhandling_foodhandlingimage_kitchenmaintenance_kitchenmaintenanceimage_sanitaryfacility_sanitaryf'),
    ]

    operations = [
        migrations.CreateModel(
            name='FSCCatalogue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('fsc_type', models.CharField(choices=[('CS', 'CS'), ('KM', 'KM'), ('SF', 'SF'), ('FH', 'FH')], default='CS', max_length=10)),
                ('status', models.CharField(choices=[('initial', 'Initial'), ('pass', 'Pass'), ('fail', 'Fail')], default='initial', max_length=10)),
            ],
            options={
                'db_table': 'table_food_compliance_safety',
            },
        ),
        migrations.CreateModel(
            name='FSCCatalogueImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=core.utils.upload_path_handler)),
                ('feedback', models.CharField(blank=True, max_length=250, null=True)),
                ('status', models.CharField(choices=[('initial', 'Initial'), ('pass', 'Pass'), ('fail', 'Fail')], default='initial', max_length=10)),
                ('cook', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fsc_catalogue_cook', to='cook.cook')),
                ('fsc_catalogue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fsc_catalogue_images', to='cook.fsccatalogue')),
            ],
            options={
                'db_table': 'table_food_compliance_images',
            },
        ),
    ]