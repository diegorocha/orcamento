# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-20 22:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orcamento', '0011_auto_20161105_0136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orcamento',
            name='ano',
            field=models.PositiveIntegerField(verbose_name='Ano'),
        ),
        migrations.AlterField(
            model_name='orcamento',
            name='mes',
            field=models.PositiveIntegerField(verbose_name='M\xeas'),
        ),
    ]
