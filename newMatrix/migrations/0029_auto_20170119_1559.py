# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-19 12:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newMatrix', '0028_auto_20170119_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newmatrix_largedesksmalldesk',
            name='LargeDeskSmallDesk_SmallDesk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SmallDesk_Desk_', to='newMatrix.newMatrix_smallDesk'),
        ),
    ]