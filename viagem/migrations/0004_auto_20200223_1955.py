# Generated by Django 2.2.10 on 2020-02-23 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viagem', '0003_auto_20200223_0139'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gastoviagem',
            options={'ordering': ['dia'], 'verbose_name': 'Gasto Viagem', 'verbose_name_plural': 'Gastos de Viagem'},
        ),
    ]
