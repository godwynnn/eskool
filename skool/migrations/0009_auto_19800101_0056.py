# Generated by Django 3.2 on 1979-12-31 23:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('skool', '0008_auto_19800101_0209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='level',
            name='teacher',
        ),
        migrations.AddField(
            model_name='teacherprofile',
            name='level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='skool.level'),
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
