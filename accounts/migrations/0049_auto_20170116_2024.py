# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-16 17:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0048_auto_20170116_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 1, 16, 20, 24, 46, 412000), null=True),
        ),
    ]
