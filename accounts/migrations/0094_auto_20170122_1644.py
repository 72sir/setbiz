# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-22 13:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0093_auto_20170122_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 1, 22, 16, 44, 10, 402000), null=True),
        ),
    ]
