# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-18 16:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newMatrix', '0014_auto_20170118_1954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newmatrix_smalldesk',
            name='smallDeskOne',
        ),
        migrations.AddField(
            model_name='newmatrix_smalldesk',
            name='smallDesk_1',
            field=models.OneToOneField(default=19, on_delete=django.db.models.deletion.CASCADE, related_name='smallDesk_1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='newmatrix_smalldesk',
            name='smallDesk_2',
            field=models.OneToOneField(default=19, on_delete=django.db.models.deletion.CASCADE, related_name='smallDesk_2', to=settings.AUTH_USER_MODEL),
        ),
    ]
