# Generated by Django 4.1.7 on 2023-02-25 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_remove_region_id_alter_region_mid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='region',
            old_name='mid',
            new_name='id',
        ),
    ]
