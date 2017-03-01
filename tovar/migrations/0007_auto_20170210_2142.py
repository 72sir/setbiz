# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-10 18:42
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tovar', '0006_auto_20170210_1756'),
    ]

    operations = [
        migrations.CreateModel(
            name='FotoTovar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, max_length=1000, upload_to='static/product/avatar/%Y/%m/', verbose_name='avatar')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='FotoTovar_product', to='tovar.Product')),
            ],
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='key_expires',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 2, 10, 21, 42, 24, 685000), null=True),
        ),
    ]