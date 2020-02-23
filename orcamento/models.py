# coding: utf-8
from __future__ import unicode_literals
from decimal import *
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Categoria(models.Model):
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categoria'
        ordering = ['descricao']
    descricao = models.CharField('Descrição', max_length=50)

    def __str__(self):
        return self.descricao


@python_2_unicode_compatible
class Moeda(models.Model):
    class Meta:
        verbose_name = 'Moeda'
        verbose_name_plural = 'Moedas'
        ordering = ['nome']
    sigla = models.CharField('Sigla', max_length=3, blank=False, null=False)
    simbolo = models.CharField('Símbolo', max_length=5, blank=False, null=False)
    nome = models.CharField('Nome', max_length=50, blank=False, null=False)

    def __str__(self):
        return self.nome


@python_2_unicode_compatible
class Orcamento(models.Model):
    class Meta:
        verbose_name = 'Orçamento'
        verbose_name_plural = 'Orçamentos'
        ordering = ['-ano', '-mes']
    ano = models.PositiveIntegerField('Ano', blank=False, null=False)
    mes = models.PositiveIntegerField('Mês', blank=False, null=False)

    @property
    def previsto(self):
        value = self.contas.aggregate(models.Sum('previsto'))
        return value.get('previsto__sum')or 0

    @property
    def atual(self):
        value = self.contas.aggregate(models.Sum('atual'))
        return value.get('atual__sum') or 0

    @property
    def a_pagar(self):
        value = Decimal(0.0)
        for conta in self.contas.all():
            value += conta.a_pagar
        return value

    @property
    def pago(self):
        value = self.contas.aggregate(models.Sum('pago'))
        return value.get('pago__sum') or 0

    @property
    def mercado_principal(self):
        value = self.mercados.filter(tipo=0).aggregate(models.Sum('valor'))
        return value.get('valor__sum') or 0


    @property
    def mercado_outros(self):
        value = self.mercados.filter(tipo=1).aggregate(models.Sum('valor'))
        return value.get('valor__sum') or 0

    def get_next_orcamento(self):
        ano = self.ano
        mes = self.mes + 1
        if mes > 12:
            mes = 1
            ano += 1
        return ano, mes

    def __str__(self):
        return '%04d/%02d' % (self.ano, self.mes)


@python_2_unicode_compatible
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
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, related_name='contas', null=True, blank=True)
    parcela_atual = models.IntegerField('Parcela', blank=True, default=1)
    parcelas = models.IntegerField('Parcelas', blank=True, default=1)
    recorrente = models.BooleanField('Recorrente', blank=True, default=False)

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
        if self.parcelas > 1:
            self.recorrente = True
        super(Conta, self).save(*args, **kwargs)

    def __str__(self):
        return '%s de %s' % (self.nome, self.orcamento)


@python_2_unicode_compatible
class EnergiaEletrica(models.Model):
    class Meta:
        verbose_name = 'Consumo de Energia Elétrica'
        verbose_name_plural = 'Consumos de Energia Elétrica'
        ordering = ('orcamento',)

    VERDE = 0
    AMARELA = 1
    VERMELHA = 2
    VERMELHA2 = 3
    BANDEIRA_CHOICES = ((VERDE, 'Verde'), (AMARELA, 'Amarela'), (VERMELHA, 'Vermelha 1'), (VERMELHA2, 'Vermelha 2'), )

    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name='energia_eletrica')
    kwh = models.IntegerField('kWh', blank=False, null=False)
    bandeira = models.IntegerField('Bandeira', choices=BANDEIRA_CHOICES, blank=True, default=VERDE)
    valor_kwh = models.DecimalField('Valor kWh', max_digits=8, decimal_places=6, blank=False, null=False)
    outros_custos = models.DecimalField('Outros Custos', max_digits=8, decimal_places=2, blank=True, default=0.0)
    valor = models.DecimalField('Valor', max_digits=8, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.valor is None:
            self.valor = self.kwh * self.valor_kwh + self.outros_custos
        super(EnergiaEletrica, self).save(*args, **kwargs)

    def __str__(self):
        return '%s de %s' % (self._meta.verbose_name, self.orcamento)
