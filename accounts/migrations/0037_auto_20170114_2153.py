# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-14 18:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0036_auto_20170114_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 1, 14, 21, 53, 27, 280000), null=True),
        ),
    ]
