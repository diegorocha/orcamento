# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-05 01:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orcamento', '0010_auto_20161105_0120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itenslista',
            name='secao',
        ),
        migrations.RemoveField(
            model_name='mercado',
            name='orcamento',
        ),
        migrations.DeleteModel(
            name='ItensLista',
        ),
        migrations.DeleteModel(
            name='Mercado',
        ),
        migrations.DeleteModel(
            name='SecaoLista',
        ),
    ]
