# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-11 17:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20170111_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 1, 11, 20, 30, 25, 192000), null=True),
        ),
    ]
