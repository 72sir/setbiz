# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-18 17:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newMatrix', '0018_auto_20170118_2007'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newmatrix_smalldesk',
            old_name='smallDesk_3',
            new_name='smallDesk_LeftPlace',
        ),
        migrations.RenameField(
            model_name='newmatrix_smalldesk',
            old_name='smallDesk_2',
            new_name='smallDesk_RightPlace',
        ),
        migrations.RenameField(
            model_name='newmatrix_smalldesk',
            old_name='smallDesk_1',
            new_name='smallDesk_UserInHead',
        ),
    ]
