# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-10 14:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0105_auto_20170209_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 2, 10, 17, 56, 55, 402000), null=True),
        ),
    ]