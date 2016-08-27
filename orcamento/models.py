# coding: utf-8
from __future__ import unicode_literals
from decimal import *
from django.db import models


class Orcamento(models.Model):
    class Meta:
        verbose_name = 'Orçamento'
        verbose_name_plural = 'Orçamentos'
    ano = models.IntegerField('Ano', blank=False, null=False)
    mes = models.IntegerField('Mês', blank=False, null=False)

    @property
    def previsto(self):
        value = self.contas.aggregate(models.Sum('previsto'))
        if value:
            return value.values()[0]

    @property
    def atual(self):
        value = self.contas.aggregate(models.Sum('atual'))
        if value:
            return value.values()[0]

    @property
    def a_pagar(self):
        value = Decimal(0.0)
        for conta in self.contas.all():
            value += conta.a_pagar
        return value

    @property
    def pago(self):
        value = self.contas.aggregate(models.Sum('pago'))
        if value:
            return value.values()[0]

    def __unicode__(self):
        return '%d/%d' % (self.ano, self.mes)


class Conta(models.Model):
    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'

    PAGAR = 0
    PAGO = 1
    ADIAR = 2

    SITUACAO_CHOICES = ((PAGAR, 'Pagar'), (PAGO, 'Pago'), (ADIAR, 'Adiar'))

    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name='contas')
    nome = models.CharField('Nome', max_length=50, blank=False, null=False)
    descricao = models.CharField('Descrição', max_length=50, blank=True, null=True)
    previsto = models.DecimalField('Valor Previsto', max_digits=8, decimal_places=2, blank=False, null=False)
    atual = models.DecimalField('Valor Atual', max_digits=8, decimal_places=2, blank=True, null=False)
    pago = models.DecimalField('Valor Pago', max_digits=8, decimal_places=2, blank=True, null=False, default=0)
    situacao = models.IntegerField('Situação', choices=SITUACAO_CHOICES, blank=True, default=PAGAR)

    @property
    def a_pagar(self):
        if self.pago:
            return self.atual - self.pago
        return self.atual

    def esta_pago(self):
        return self.a_pagar <= 0

    def save(self, *args, **kwargs):
        if self.atual is None:
            self.atual = self.previsto
        if self.esta_pago():
            self.situacao = Conta.PAGO
        super(Conta, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s de %s' % (self.nome, self.orcamento)
