# Generated by Django 4.1.7 on 2023-02-23 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_region_alter_userbase_address_alter_userbase_image_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='region',
            old_name='addresAll',
            new_name='addressAll',
        ),
    ]
