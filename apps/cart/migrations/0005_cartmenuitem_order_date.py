# Generated by Django 3.2.12 on 2022-10-17 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_cartmenuitem_save_for_later'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartmenuitem',
            name='order_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
