# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-27 10:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiltacam', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='current',
            field=models.ImageField(upload_to='cameras'),
        ),
    ]
