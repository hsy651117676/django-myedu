# Generated by Django 4.1.7 on 2023-02-25 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_rename_mid_region_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='region',
            old_name='id',
            new_name='mid',
        ),
    ]
