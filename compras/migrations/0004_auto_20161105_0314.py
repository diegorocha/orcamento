# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-05 03:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0003_auto_20161105_0305'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itenslista',
            options={'ordering': ('secao', 'ordem', 'descricao'), 'verbose_name': 'Item', 'verbose_name_plural': 'Itens'},
        ),
        migrations.AddField(
            model_name='itenslista',
            name='ordem',
            field=models.IntegerField(blank=True, default=999, verbose_name='Ordem'),
        ),
    ]