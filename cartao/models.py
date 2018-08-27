# coding: utf-8
from copy import copy

from django.core.exceptions import ValidationError
from django.db import models
from orcamento.models import Orcamento, Categoria
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Bandeira(models.Model):
    class Meta:
        verbose_name = 'Bandeira'
        verbose_name_plural = 'Bandeira'
    descricao = models.CharField('Descrição', max_length=50, blank=False, null=False)

    def __str__(self):
        return self.descricao


@python_2_unicode_compatible
class Cartao(models.Model):
    class Meta:
        verbose_name = 'Cartão'
        verbose_name_plural = 'Cartões'
    bandeira = models.ForeignKey(Bandeira, on_delete=models.CASCADE, related_name='cartoes')
    descricao = models.CharField('Descrição', max_length=50, blank=True, null=True)
    limite = models.DecimalField('Valor em Dolar', max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.descricao, self.bandeira)


@python_2_unicode_compatible
class Fatura(models.Model):
    class Meta:
        verbose_name = 'Fatura'
        verbose_name_plural = 'Faturas'
    cartao = models.ForeignKey(Cartao, on_delete=models.CASCADE, related_name='faturas')
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name='faturas')
    aberta = models.BooleanField('Aberta', blank=True, default=True)
    valor_final = models.DecimalField('Valor Final', max_digits=8, decimal_places=2, blank=True, null=True)

    @property
    def descricao(self):
        return '%s %s' % (self.cartao.descricao, self.orcamento)

    @property
    def valor_inicial(self):
        value = self.compras.aggregate(models.Sum('valor_inicial'))
        return value.get('valor_inicial__sum') or 0

    def get_compras_proxima_fatura(self, compras=None):
        if compras is None:
            compras = self.compras.all()
        novas_compras = []
        total = {
            'valor_real': 0,
            'valor_dolar': 0,
            'valor_fatura': 0
        }
        for compra in compras:
            nova_compra = None
            if compra.recorrente:
                nova_compra = copy(compra)
            if compra.parcelas > 1 and compra.parcela_atual < compra.parcelas:
                nova_compra = copy(compra)
                if nova_compra.valor_parcela:
                    # Tratamento de compras parceladas com valor de inicial diferente
                    nova_compra.valor_real = nova_compra.valor_parcela
                    nova_compra.valor_parcela = None
                nova_compra.parcela_atual += 1
            if nova_compra:
                total['valor_real'] += nova_compra.valor_real or 0
                total['valor_dolar'] += nova_compra.valor_dolar or 0
                total['valor_fatura'] += nova_compra.valor_fatura or 0
                novas_compras.append(nova_compra)
        return novas_compras, total

    def _get_nome_fatura(self, n):
        cartao = self.cartao
        ano = self.orcamento.ano
        mes = self.orcamento.mes + n
        if mes > 12:
            mes = mes % 12
            ano += int(mes / 12)
        return '%s - %d/%02d' % (cartao, ano, mes)

    def get_proximas_faturas(self, qtd=1):
        if not self.aberta:
            return []
        faturas = []
        compras = self.compras.all()
        for i in range(1, qtd + 1):
            compras, totais = self.get_compras_proxima_fatura(compras)
            faturas.append({
                'fatura': self._get_nome_fatura(i),
                'compras': compras,
                'total': totais
            })
        return faturas

    def __str__(self):
        return '%s - %s' % (self.cartao, self.orcamento)


@python_2_unicode_compatible
class CompraCartao(models.Model):
    class Meta:
        verbose_name = 'Compra Cartão'
        verbose_name_plural = 'Compras Cartão'
    fatura = models.ForeignKey(Fatura, on_delete=models.CASCADE, related_name='compras')
    descricao = models.CharField('Descrição', max_length=50, blank=False, null=False)
    descricao_fatura = models.CharField('Descrição Fatura', max_length=50, blank=True, null=True)
    valor_real = models.DecimalField('Valor em Real', max_digits=8, decimal_places=2, blank=True, null=True)
    valor_dolar = models.DecimalField('Valor em Dolar', max_digits=8, decimal_places=2, blank=True, null=True)
    valor_inicial = models.DecimalField('Valor Inicial', max_digits=8, decimal_places=2, blank=True, null=False)
    valor_fatura = models.DecimalField('Valor Fatura', max_digits=8, decimal_places=2, blank=True, null=True)
    valor_final = models.DecimalField('Valor Final', max_digits=8, decimal_places=2, blank=True, null=True)
    valor_parcela = models.DecimalField('Valor Parcela', max_digits=8, decimal_places=2, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, related_name='compras_cartao', null=True, blank=True)
    parcelas = models.IntegerField('Parcelas', blank=True, default=1)
    parcela_atual = models.IntegerField('Parcela', blank=True, default=1)
    recorrente = models.BooleanField('Recorrente', blank=True, default=False)

    def save(self, *args, **kwargs):
        if not self.valor_inicial:
            self.valor_inicial = self.valor_real
        if self.fatura and not self.fatura.aberta:
            raise ValidationError('Fatura %s já está fechada' % self.fatura)
        super(CompraCartao, self).save(*args, **kwargs)

    def __str__(self):
        return '%s de %s' % (self.descricao, self.fatura)


@python_2_unicode_compatible
class SMSCartao(models.Model):
    class Meta:
        verbose_name = 'SMS Cartão'
        verbose_name_plural = 'SMSs Cartão'
        ordering = ['criado']
    texto = models.TextField(unique=True)
    criado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.texto


@python_2_unicode_compatible
class CartaoAliasSMS(models.Model):
    cartao = models.ForeignKey(Cartao, on_delete=models.CASCADE, related_name='alias')
    texto = models.CharField(max_length=50)

    def __str__(self):
        return '%s @ %s' % (self.cartao, self.texto)
