# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-16 17:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0047_auto_20170116_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 1, 16, 20, 22, 45, 72000), null=True),
        ),
    ]
