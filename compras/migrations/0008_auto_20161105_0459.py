# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-05 04:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0007_itenslista_ativo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itemcompra',
            old_name='itens',
            new_name='item',
        ),
    ]