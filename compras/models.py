# coding: utf-8
from __future__ import unicode_literals
from django.db import models
from orcamento.models import Orcamento


class Mercado(models.Model):
    class Meta:
        verbose_name = 'Mercado'
        verbose_name_plural = 'Mercado'
        ordering = ('orcamento', 'tipo')

    PRINCIPAL = 0
    OUTROS = 1

    TIPO_CHOICES = ((PRINCIPAL, 'Principal'), (OUTROS, 'Outros'), )

    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name='mercados')
    descricao = models.CharField('Descrição', max_length=50, blank=True, null=True)
    tipo = models.IntegerField('Tipo', choices=TIPO_CHOICES, blank=True, default=PRINCIPAL)
    valor = models.DecimalField('Valor Atual', max_digits=8, decimal_places=2, )
    itens = models.IntegerField('Itens', blank=True, null=True)

    def __str__(self):
        return 'Mercado de %s' % (self.orcamento)


class SecaoLista(models.Model):
    class Meta:
        verbose_name = 'Seção'
        verbose_name_plural = 'Seções'
        ordering = ('ordem', 'descricao')
    descricao = models.CharField('Descrição', max_length=50)
    ordem = models.IntegerField('Ordem', blank=True, default=999)

    def __str__(self):
        return self.descricao


class ItensLista(models.Model):
    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Itens'
        ordering = ('secao', 'ordem', 'descricao')
    secao = models.ForeignKey(SecaoLista, related_name='itens', on_delete=models.CASCADE)
    ordem = models.IntegerField('Ordem', blank=True, default=999)
    descricao = models.CharField('Descrição', max_length=50)
    quantidade_sugerida = models.IntegerField('Qtd Sugerida', blank=True, default=1)
    unidade = models.CharField('Unidade', max_length=20, blank=True, default='UN')
    ativo = models.BooleanField(blank=True, default=True)

    @property
    def quantidade(self):
        if self.quantidade_sugerida and self.unidade:
            return '%d %s' % (self.quantidade_sugerida, self.unidade)

    def __str__(self):
        return self.descricao


class ListaCompras(models.Model):
    class Meta:
        verbose_name = 'Lista'
        verbose_name_plural = 'Listas'
        ordering = ('orcamento', )
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name='lista_compras')
    itens = models.ManyToManyField(ItensLista, through='ItemCompra')

    def save(self, *args, **kwargs):
        super(ListaCompras, self).save(*args, **kwargs)
        if self.itens and self.itens.count() == 0:
            # Adiciona todos os itens padrões atuais
            for item in ItensLista.objects.filter(ativo=True):
                item_compra = ItemCompra(item=item, lista=self)
                item_compra.comprar = False
                item_compra.comprado = False
                item_compra.save()

    def __str__(self):
        return 'Lista de compras de %s' % self.orcamento


class ItemCompra(models.Model):
    class Meta:
        ordering = ('lista', 'item')
    lista = models.ForeignKey(ListaCompras, on_delete=models.CASCADE)
    item = models.ForeignKey(ItensLista, on_delete=models.CASCADE)
    quantidade_sugerida = models.IntegerField('Qtd Sugerida', blank=True, null=True)
    unidade = models.CharField('Unidade', max_length=20, blank=True, null=True)
    comprar = models.BooleanField(blank=True, default=True)
    comprado = models.BooleanField(blank=True, default=False)

    @property
    def quantidade(self):
        if self.quantidade_sugerida or self.unidade:
            qtd = self.quantidade_sugerida or self.item.quantidade_sugerida
            unidade = self.unidade or self.item.unidade
            return '%d %s' % (qtd, unidade)
        return self.item.quantidade

    def __str__(self):
        return '%s de %s' % (self.item, self.lista.orcamento)
