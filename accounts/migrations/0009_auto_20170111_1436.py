# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-11 11:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_user_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='parent',
        ),
        migrations.AddField(
            model_name='user',
            name='parent',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]