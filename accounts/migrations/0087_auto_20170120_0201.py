# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-19 23:01
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0086_auto_20170119_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='structure',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 1, 20, 2, 1, 2, 686000), null=True),
        ),
    ]
