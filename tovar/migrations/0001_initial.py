# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-05 15:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('destination', models.BooleanField(default=False)),
                ('company', models.BooleanField(default=False)),
                ('type', models.BooleanField(default=False)),
                ('model', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_attribure', to='tovar.Attribute')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, max_length=1000, upload_to='static/product/avatar/%Y/%m/', verbose_name='avatar')),
                ('name', models.CharField(max_length=150)),
                ('title', models.CharField(max_length=400)),
                ('text', models.TextField()),
                ('price', models.PositiveIntegerField(default=0)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('company', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_product', to='tovar.Attribute')),
                ('destination', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='destination_producrt', to='tovar.Attribute')),
                ('model', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='model_product', to='tovar.Attribute')),
                ('type', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='type_product', to='tovar.Attribute')),
            ],
        ),
    ]
