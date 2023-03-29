# Generated by Django 3.2.13 on 2022-05-25 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country_id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('country_name', models.CharField(max_length=120, null=True)),
                ('iso2', models.CharField(max_length=2, null=True)),
                ('iso3', models.CharField(max_length=3, null=True)),
                ('isd_code', models.CharField(blank=True, max_length=20, null=True)),
                ('currency', models.CharField(blank=True, max_length=4, null=True)),
                ('latitude', models.CharField(blank=True, max_length=15, null=True)),
                ('longitude', models.CharField(blank=True, max_length=15, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Countries',
                'db_table': 'table_country',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('state_id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('state_name', models.CharField(max_length=120, null=True)),
                ('state_code', models.CharField(blank=True, max_length=20, null=True)),
                ('latitude', models.CharField(blank=True, max_length=15, null=True)),
                ('longitude', models.CharField(blank=True, max_length=15, null=True)),
                ('active', models.BooleanField(default=True)),
                ('country_id', models.ForeignKey(blank=True, db_column='country_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='country_states', to='snippets.country')),
            ],
            options={
                'verbose_name_plural': 'States',
                'db_table': 'table_states',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('city_id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('city_name', models.CharField(max_length=120, null=True)),
                ('latitude', models.CharField(blank=True, max_length=15, null=True)),
                ('longitude', models.CharField(blank=True, max_length=15, null=True)),
                ('active', models.BooleanField(default=True)),
                ('country_id', models.ForeignKey(blank=True, db_column='country_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='country_cities', to='snippets.country')),
                ('state_id', models.ForeignKey(blank=True, db_column='state_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='state_cities', to='snippets.state')),
            ],
            options={
                'verbose_name_plural': 'Cities',
                'db_table': 'table_cities',
            },
        ),
    ]
