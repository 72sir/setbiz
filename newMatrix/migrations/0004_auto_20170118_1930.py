# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-18 16:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newMatrix', '0003_auto_20170118_1930'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newmatrix_smalldesk',
            name='smallDesk_1',
        ),
        migrations.RemoveField(
            model_name='newmatrix_smalldesk',
            name='smallDesk_2',
        ),
        migrations.RemoveField(
            model_name='newmatrix_smalldesk',
            name='smallDesk_3',
        ),
    ]
