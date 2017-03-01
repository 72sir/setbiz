# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-12 15:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_auto_20170112_1832'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='passWallet',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 1, 12, 18, 53, 54, 339000), null=True),
        ),
    ]
