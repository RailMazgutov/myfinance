# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-17 18:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_total', models.DecimalField(decimal_places=2, max_digits=30)),
            ],
        ),
        migrations.CreateModel(
            name='Charge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='charges', to='finance.Account')),
            ],
        ),
    ]