# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-18 17:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0076_auto_20170118_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 1, 18, 20, 19, 54, 550000), null=True),
        ),
    ]
