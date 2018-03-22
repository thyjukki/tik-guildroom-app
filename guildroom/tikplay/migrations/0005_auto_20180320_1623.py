# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-20 16:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tikplay', '0004_song_audio_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_id', models.TextField(default='')),
                ('added_by', models.TextField(default='')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='song',
            name='added_by',
            field=models.TextField(default=''),
        ),
    ]