# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-18 16:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0068_auto_20170118_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 1, 18, 19, 46, 50, 63000), null=True),
        ),
    ]
