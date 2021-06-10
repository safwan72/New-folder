# Generated by Django 3.1.6 on 2021-03-12 16:11

import blogger.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogger', '0010_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blogger.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='like',
            name='like_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blogger.user'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_id_slug', models.SlugField(default=blogger.utils.get_unique_path, max_length=20, unique=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('favourite_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogger.post')),
            ],
        ),
    ]