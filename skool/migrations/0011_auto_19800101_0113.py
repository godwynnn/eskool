# Generated by Django 3.2 on 1980-01-01 00:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skool', '0010_auto_19800101_0013'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentprofile',
            old_name='student_bday',
            new_name='birthday',
        ),
        migrations.RenameField(
            model_name='studentprofile',
            old_name='student_email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='studentprofile',
            old_name='student_id',
            new_name='id_no',
        ),
        migrations.RenameField(
            model_name='teacherprofile',
            old_name='teacher_email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='teacherprofile',
            old_name='teacher_id',
            new_name='id_no',
        ),
    ]
