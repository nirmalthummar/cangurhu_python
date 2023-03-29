# Generated by Django 3.2.13 on 2022-07-21 07:05

import core.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cook', '0009_auto_20220720_0935'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodHandling',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=120)),
                ('quantity', models.IntegerField(help_text='Total number of objects')),
                ('feedback', models.CharField(blank=True, max_length=250, null=True)),
                ('status', models.CharField(choices=[('initial', 'Initial'), ('pass', 'Pass'), ('fail', 'Fail')], default='initial', max_length=10)),
                ('cook', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='food_handling', to='cook.cook')),
            ],
            options={
                'db_table': 'table_food_handling',
            },
        ),
        migrations.CreateModel(
            name='KitchenMaintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=120)),
                ('quantity', models.IntegerField(help_text='Total number of objects')),
                ('feedback', models.CharField(blank=True, max_length=250, null=True)),
                ('status', models.CharField(choices=[('initial', 'Initial'), ('pass', 'Pass'), ('fail', 'Fail')], default='initial', max_length=10)),
                ('cook', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kitchen_maintenance', to='cook.cook')),
            ],
            options={
                'db_table': 'table_kitchen_maintenance',
            },
        ),
        migrations.CreateModel(
            name='SanitaryFacility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=120)),
                ('quantity', models.IntegerField(help_text='Total number of objects')),
                ('feedback', models.CharField(blank=True, max_length=250, null=True)),
                ('status', models.CharField(choices=[('initial', 'Initial'), ('pass', 'Pass'), ('fail', 'Fail')], default='initial', max_length=10)),
                ('cook', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sanitary_facility', to='cook.cook')),
            ],
            options={
                'db_table': 'table_sanitary_facility',
            },
        ),
        migrations.CreateModel(
            name='SanitaryFacilityImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=core.utils.upload_path_handler)),
                ('feedback', models.CharField(blank=True, max_length=250, null=True)),
                ('status', models.CharField(choices=[('initial', 'Initial'), ('pass', 'Pass'), ('fail', 'Fail')], default='initial', max_length=10)),
                ('sanitary_facility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sanitary_facility_images', to='cook.sanitaryfacility')),
            ],
            options={
                'db_table': 'table_sanitary_facility_images',
            },
        ),
        migrations.CreateModel(
            name='KitchenMaintenanceImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=core.utils.upload_path_handler)),
                ('feedback', models.CharField(blank=True, max_length=250, null=True)),
                ('status', models.CharField(choices=[('initial', 'Initial'), ('pass', 'Pass'), ('fail', 'Fail')], default='initial', max_length=10)),
                ('kitchen_maintenance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kitchen_maintenance_images', to='cook.kitchenmaintenance')),
            ],
            options={
                'db_table': 'table_kitchen_maintenance_images',
            },
        ),
        migrations.CreateModel(
            name='FoodHandlingImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=core.utils.upload_path_handler)),
                ('feedback', models.CharField(blank=True, max_length=250, null=True)),
                ('status', models.CharField(choices=[('initial', 'Initial'), ('pass', 'Pass'), ('fail', 'Fail')], default='initial', max_length=10)),
                ('food_handling', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='food_handling_images', to='cook.foodhandling')),
            ],
            options={
                'db_table': 'table_food_handling_images',
            },
        ),
    ]
