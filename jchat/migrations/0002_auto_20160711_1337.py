# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-11 13:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jchat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 11, 13, 37, 26, 957563)),
        ),
    ]