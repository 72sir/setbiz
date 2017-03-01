# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-18 16:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newMatrix', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newmatrix_smalldesk',
            name='object_id',
        ),
        migrations.AddField(
            model_name='newmatrix_smalldesk',
            name='smallDesk_1',
            field=models.PositiveIntegerField(default=19),
        ),
        migrations.AddField(
            model_name='newmatrix_smalldesk',
            name='smallDesk_2',
            field=models.PositiveIntegerField(default=19),
        ),
        migrations.AddField(
            model_name='newmatrix_smalldesk',
            name='smallDesk_3',
            field=models.PositiveIntegerField(default=19),
        ),
    ]
