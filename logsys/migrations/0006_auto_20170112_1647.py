# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-12 13:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logsys', '0005_auto_20170112_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infoproduct',
            name='InfoProduct_date',
            field=models.DateField(default=datetime.datetime(2017, 1, 12, 16, 47, 31, 656000)),
        ),
    ]
