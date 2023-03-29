# Generated by Django 3.2.13 on 2022-09-16 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courier', '0013_alter_courierorder_cook_status'),
        ('rating', '0002_auto_20220907_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='cookfeedback',
            name='courier_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courier_rating', to='courier.courier'),
        ),
    ]
