# Generated by Django 2.1.15 on 2020-06-07 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0003_recipe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='time_minute',
            new_name='time_minutes',
        ),
    ]
