# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-13 20:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_auto_20170113_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 1, 13, 23, 40, 10, 973000), null=True),
        ),
    ]
