# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 20:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0104_auto_20170209_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 2, 9, 23, 34, 4, 748000), null=True),
        ),
    ]
