# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-14 12:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0002_auto_20160914_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetings',
            name='TIME',
            field=models.TimeField(default='13:36', verbose_name='TIME'),
        ),
    ]
