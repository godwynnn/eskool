# Generated by Django 3.2 on 2021-08-30 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skool', '0024_auto_20210830_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsfeed',
            name='category',
            field=models.CharField(blank=True, choices=[('News', 'News'), ('Tech', 'Tech'), ('Business', 'Business'), ('Lifestyle', 'Lifestyle'), ('Feature', 'Feature')], default='News', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='newsfeed',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='newsfeed',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='newsfeed',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='skool.Tag'),
        ),
    ]
