# Generated by Django 3.2.13 on 2022-09-20 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0011_auto_20220920_1218'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ConstantRange',
            new_name='ConstantRangeDistance',
        ),
        migrations.AlterModelTable(
            name='constantrangedistance',
            table='table_constantrangedistance',
        ),
    ]