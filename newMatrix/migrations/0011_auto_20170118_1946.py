# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-18 16:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newMatrix', '0010_auto_20170118_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newmatrix_smalldesk',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='newmatrix_smalldesk',
            name='object_id',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='newmatrix_smalldesk',
            name='tag',
            field=models.SlugField(),
        ),
    ]
