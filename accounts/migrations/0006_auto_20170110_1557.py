# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-10 12:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20170110_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='adress',
            field=models.CharField(max_length=160, null=True, verbose_name='adress'),
        ),
    ]