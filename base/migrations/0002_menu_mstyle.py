# Generated by Django 4.1.7 on 2023-02-19 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='mstyle',
            field=models.CharField(default='', max_length=150, verbose_name='style'),
        ),
    ]
