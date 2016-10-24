# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-24 19:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='charge',
            name='_account',
        ),
        migrations.AddField(
            model_name='charge',
            name='_date',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='_total',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
        migrations.AlterField(
            model_name='charge',
            name='_value',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
