# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 14:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tovar', '0002_orderproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='payment',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='key_expires',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 2, 9, 17, 54, 31, 399000), null=True),
        ),
    ]
