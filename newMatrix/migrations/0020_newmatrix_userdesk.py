# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-18 17:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newMatrix', '0019_auto_20170118_2009'),
    ]

    operations = [
        migrations.CreateModel(
            name='newMatrix_UserDesk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UserDesk_Desk', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='UserDesk_Desk', to='newMatrix.newMatrix_smallDesk')),
                ('UserDesk_User', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='UserDesk_User', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
