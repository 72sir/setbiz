# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-12 16:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_auto_20170112_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 1, 12, 19, 10, 55, 912000), null=True),
        ),
    ]