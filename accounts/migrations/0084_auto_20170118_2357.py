# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-18 20:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0083_auto_20170118_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 1, 18, 23, 57, 41, 467000), null=True),
        ),
    ]
