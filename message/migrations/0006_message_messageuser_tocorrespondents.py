# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-22 13:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0005_auto_20170122_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='message_messageuser',
            name='toCorrespondents',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='toUser_4', to='message.message_correspondents'),
            preserve_default=False,
        ),
    ]