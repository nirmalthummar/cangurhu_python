# Generated by Django 3.2.13 on 2022-09-22 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0017_auto_20220922_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagetexts',
            name='message_text',
            field=models.TextField(),
        ),
    ]
