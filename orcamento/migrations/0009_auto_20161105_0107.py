# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-05 01:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orcamento', '0008_auto_20161105_0040'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItensLista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=50, verbose_name='Descri\xe7\xe3o')),
                ('quantidade_sugerida', models.IntegerField(blank=True, default=1, verbose_name='Qtd Sugerida')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Itens',
            },
        ),
        migrations.AlterModelOptions(
            name='secaolista',
            options={'ordering': ('ordem', 'descricao'), 'verbose_name': 'Se\xe7\xe3o', 'verbose_name_plural': 'Se\xe7\xf5es'},
        ),
        migrations.AddField(
            model_name='itenslista',
            name='secao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='orcamento.SecaoLista'),
        ),
    ]