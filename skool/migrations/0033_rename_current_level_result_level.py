# Generated by Django 3.2 on 2022-04-16 22:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skool', '0032_auto_19800101_0025'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result',
            old_name='current_level',
            new_name='level',
        ),
    ]