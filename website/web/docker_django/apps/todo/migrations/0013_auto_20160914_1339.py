# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-14 12:39
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0012_auto_20160914_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2016, 9, 14, 12, 39, 23, 526516, tzinfo=utc)),
        ),
    ]
