# Generated by Django 2.2.4 on 2019-08-14 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0012_auto_20161111_0530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemcompra',
            name='comprado',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='itemcompra',
            name='comprar',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='itenslista',
            name='ativo',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]