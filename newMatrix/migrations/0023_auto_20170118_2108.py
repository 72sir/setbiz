# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-18 18:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newMatrix', '0022_auto_20170118_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newmatix_largedesk',
            name='largeDesk_LeftDesk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='largeDeskTwoDesk', to='newMatrix.newMatrix_smallDesk'),
        ),
        migrations.AlterField(
            model_name='newmatix_largedesk',
            name='largeDesk_RightDesk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='largeDeskOneDesk', to='newMatrix.newMatrix_smallDesk'),
        ),
        migrations.AlterField(
            model_name='newmatrix_userdesk',
            name='UserDesk_Desk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='UserDesk_Desk', to='newMatrix.newMatrix_smallDesk', unique=True),
        ),
        migrations.AlterField(
            model_name='newmatrix_userdesk',
            name='UserDesk_User',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='UserDesk_User', to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
