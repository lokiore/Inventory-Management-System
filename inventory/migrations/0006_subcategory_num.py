# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-30 14:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_category_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='num',
            field=models.IntegerField(default=0, unique=True),
            preserve_default=False,
        ),
    ]