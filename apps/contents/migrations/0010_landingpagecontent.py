# Generated by Django 3.2.12 on 2022-11-01 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0009_auto_20221006_0113'),
    ]

    operations = [
        migrations.CreateModel(
            name='LandingPageContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cook_heading', models.CharField(blank=True, max_length=150, null=True)),
                ('cook_body', models.CharField(blank=True, max_length=300, null=True)),
                ('courier_heading', models.CharField(blank=True, max_length=150, null=True)),
                ('courier_body', models.CharField(blank=True, max_length=300, null=True)),
                ('customer_heading', models.CharField(blank=True, max_length=150, null=True)),
                ('customer_body', models.CharField(blank=True, max_length=300, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Active'), (0, 'Inactive'), (2, 'Delete')], default=1)),
            ],
            options={
                'db_table': 'table_landing_page_content',
            },
        ),
    ]
