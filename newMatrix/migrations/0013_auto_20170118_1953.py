# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-18 16:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newMatrix', '0012_remove_newmatrix_smalldesk_object_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newmatrix_smalldesk',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='newmatrix_smalldesk',
            name='tag',
        ),
        migrations.AddField(
            model_name='newmatrix_smalldesk',
            name='smallDeskOne',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]