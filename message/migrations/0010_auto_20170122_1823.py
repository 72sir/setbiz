# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-22 15:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('message', '0009_remove_massege_user_user_two'),
    ]

    operations = [
        migrations.AddField(
            model_name='massege_user',
            name='user_two',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_two', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='massege_user',
            name='user_one',
        ),
        migrations.AddField(
            model_name='massege_user',
            name='user_one',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_one', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
