# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-05 04:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orcamento', '0011_auto_20161105_0136'),
        ('compras', '0004_auto_20161105_0314'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemCompra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itens', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compras.ItensLista')),
            ],
        ),
        migrations.CreateModel(
            name='ListaCompras',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itens', models.ManyToManyField(through='compras.ItemCompra', to='compras.ItensLista')),
                ('orcamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lista_compras', to='orcamento.Orcamento')),
            ],
            options={
                'ordering': ('orcamento',),
                'verbose_name': 'Lista',
                'verbose_name_plural': 'Listas',
            },
        ),
        migrations.AddField(
            model_name='itemcompra',
            name='lista',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compras.ListaCompras'),
        ),
    ]
