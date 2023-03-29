# Generated by Django 3.2.13 on 2022-06-12 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0001_initial'),
        ('contents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('banner_id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('banner_image', models.ImageField(upload_to='banners/')),
                ('send_to_all', models.BooleanField(default=False)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('town', models.CharField(blank=True, max_length=50, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=15, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Active'), (0, 'Inactive'), (2, 'Delete')], default=1)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='banner_countries', to='snippets.country')),
            ],
            options={
                'verbose_name': 'Banner',
                'verbose_name_plural': 'Banners',
                'db_table': 'table_banners',
            },
        ),
    ]
