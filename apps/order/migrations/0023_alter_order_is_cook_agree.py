# Generated by Django 3.2.12 on 2022-11-02 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0022_order_is_cook_agree'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='is_cook_agree',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
