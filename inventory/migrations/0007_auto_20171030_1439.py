# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-30 14:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_subcategory_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='num',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='num',
        ),
    ]
