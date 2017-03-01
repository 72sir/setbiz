# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-10 14:56
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tovar', '0005_auto_20170209_2334'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatrixProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MatrixProduct_product', to='tovar.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Matrix_product_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='key_expires',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 2, 10, 17, 56, 55, 420000), null=True),
        ),
    ]