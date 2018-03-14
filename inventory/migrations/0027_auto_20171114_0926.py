# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-14 09:26
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0026_order_profit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Localization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_country', models.CharField(default=b'qwe', max_length=100)),
                ('c_currency', models.CharField(default=b'$', max_length=1)),
                ('c_timezone', models.CharField(default=b'wer', max_length=100)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='businessprofile',
            name='c_address',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='businessprofile',
            name='c_country',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='businessprofile',
            name='c_currency',
            field=models.CharField(default=b'', max_length=1),
        ),
        migrations.AlterField(
            model_name='businessprofile',
            name='c_email',
            field=models.EmailField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='businessprofile',
            name='c_name',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='businessprofile',
            name='c_phone',
            field=models.IntegerField(validators=[django.core.validators.RegexValidator(code=b'invalid_username', message=b"Phone number must be entered in the format: '+91##########'.", regex=b'^[1-9][0-9]{9}$')]),
        ),
        migrations.AlterField(
            model_name='businessprofile',
            name='c_timezone',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
