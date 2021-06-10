# Generated by Django 3.1.6 on 2021-03-18 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogger', '0013_auto_20210314_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='custom_stage',
            field=models.CharField(blank=True, max_length=48, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='occupation',
            field=models.CharField(blank=True, max_length=72, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='template_name',
            field=models.CharField(choices=[('l', 'Light'), ('d', 'Dark')], default='l', max_length=2),
        ),
    ]
