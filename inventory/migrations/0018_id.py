# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-07 18:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0017_auto_20171107_1349'),
    ]

    operations = [
        migrations.CreateModel(
            name='ID',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
    ]
