# Generated by Django 3.1.6 on 2021-02-15 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveAdminModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=64)),
                ('base_url', models.CharField(max_length=32)),
                ('is_active', models.BooleanField(default=True)),
                ('icon_name', models.CharField(default='fa fa-building', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ActiveCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254)),
                ('title', models.CharField(blank=True, max_length=64, null=True)),
                ('tagline', models.CharField(blank=True, max_length=128, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('about', models.TextField(blank=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
