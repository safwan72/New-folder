# Generated by Django 3.1 on 2021-04-15 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogger', '0016_auto_20210331_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='goals',
            field=models.ManyToManyField(to='blogger.Goal'),
        ),
    ]