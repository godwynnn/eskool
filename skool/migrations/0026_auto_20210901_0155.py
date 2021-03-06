# Generated by Django 3.2 on 2021-09-01 00:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('skool', '0025_auto_20210830_1154'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('date_ordered', models.DateTimeField(auto_now=True)),
                ('carts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='skool.cart')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='skool.studentprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('price', models.IntegerField(default=0)),
                ('status', models.CharField(blank=True, choices=[('Premium', 'Premuim'), ('Free', 'Free')], default='Premium', max_length=200, null=True)),
                ('url', models.URLField(blank=True, max_length=2000, null=True)),
                ('description', models.CharField(blank=True, max_length=10000, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_added'],
            },
        ),
        migrations.DeleteModel(
            name='Bookstore',
        ),
        migrations.AlterField(
            model_name='newsfeed',
            name='tags',
            field=models.ManyToManyField(blank=True, to='skool.Tag'),
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ManyToManyField(to='skool.Product'),
        ),
    ]
