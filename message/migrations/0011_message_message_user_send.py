# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-22 15:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('message', '0010_auto_20170122_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='message_message',
            name='user_send',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
