# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-18 20:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newMatrix', '0026_auto_20170118_2340'),
    ]

    operations = [
        migrations.CreateModel(
            name='newMatrix_LargeDeskSmallDesk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UserLargeDesk_Desk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='LargeDesk_Desk_', to='newMatrix.newMatix_largeDesk')),
                ('UserLargeDesk_User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SmallDesk_Desk_', to='newMatrix.newMatrix_UserDesk')),
            ],
        ),
    ]
