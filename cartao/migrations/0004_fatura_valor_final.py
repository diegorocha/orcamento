# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-05-06 18:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartao', '0003_fatura_aberta'),
    ]

    operations = [
        migrations.AddField(
            model_name='fatura',
            name='valor_final',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Valor Final'),
        ),
    ]
