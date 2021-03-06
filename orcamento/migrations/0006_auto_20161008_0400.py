# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-08 04:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orcamento', '0005_auto_20160827_2241'),
    ]

    operations = [
        migrations.AddField(
            model_name='conta',
            name='parcela_atual',
            field=models.IntegerField(blank=True, default=1, verbose_name='Parcela'),
        ),
        migrations.AddField(
            model_name='conta',
            name='parcelas',
            field=models.IntegerField(blank=True, default=1, verbose_name='Parcelas'),
        ),
        migrations.AddField(
            model_name='conta',
            name='recorrente',
            field=models.BooleanField(default=False, verbose_name='Recorrente'),
        ),
    ]
