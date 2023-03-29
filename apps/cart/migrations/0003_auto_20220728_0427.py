# Generated by Django 3.2.13 on 2022-07-28 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_alter_cart_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartmenuitem',
            name='size',
        ),
        migrations.RemoveField(
            model_name='cartmenuitem',
            name='quantity',
        ),
        migrations.AddField(
            model_name='cartmenuitem',
            name='quantity',
            field=models.JSONField(default=list),
        ),
    ]
