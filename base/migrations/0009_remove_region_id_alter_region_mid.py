# Generated by Django 4.1.7 on 2023-02-25 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_rename_addresall_region_addressall'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='region',
            name='id',
        ),
        migrations.AlterField(
            model_name='region',
            name='mid',
            field=models.CharField(default='', max_length=12, primary_key=True, serialize=False, verbose_name='mid'),
        ),
    ]
