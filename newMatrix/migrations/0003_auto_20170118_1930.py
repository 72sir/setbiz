# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-18 16:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newMatrix', '0002_auto_20170118_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newmatrix_smalldesk',
            name='smallDesk_2',
            field=models.PositiveIntegerField(default=20),
        ),
        migrations.AlterField(
            model_name='newmatrix_smalldesk',
            name='smallDesk_3',
            field=models.PositiveIntegerField(default=21),
        ),
    ]
