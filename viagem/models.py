from django.db import models
from django.db.models import Sum
from django.utils.encoding import python_2_unicode_compatible

from cartao.models import Fatura
from orcamento.models import Orcamento, Categoria, Moeda


@python_2_unicode_compatible
class Viagem(models.Model):
    class Meta:
        verbose_name = 'Viagem'
        verbose_name_plural = 'Viagens'
        ordering = ['-inicio', '-fim']
    descricao = models.CharField('Descrição', max_length=50, blank=False, null=False)
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name='viagens', blank=True, null=True)
    inicio = models.DateField('Início', blank=False)
    fim = models.DateField('Fim', blank=False)

    @property
    def custo_total(self):
        return self.gastos.aggregate(total=Sum('valor_real'))['total']

    def __str__(self):
        return self.descricao + self.inicio.strftime(' %Y/%m')


@python_2_unicode_compatible
class GastoViagem(models.Model):
    class Meta:
        verbose_name = 'Gasto Viagem'
        verbose_name_plural = 'Gastos de Viagem'
        ordering = ['dia',]
    viagem = models.ForeignKey(Viagem, on_delete=models.CASCADE, related_name='gastos')
    dia = models.DateField('Dia', blank=False, null=False)
    descricao = models.CharField('Descrição', max_length=50, blank=False, null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='gastos_viagem')
    valor_real = models.DecimalField('Valor em Reais', max_digits=8, decimal_places=2, blank=False, null=False)
    valor_dolar = models.DecimalField('Valor em Dólares', max_digits=8, decimal_places=2, blank=True, null=True)
    valor_moeda = models.DecimalField('Valor na moeda local', max_digits=8, decimal_places=2, blank=True, null=True)
    moeda = models.ForeignKey(Moeda, on_delete=models.CASCADE, related_name='gastos_viagem', blank=False)
    taxa_conversao = models.DecimalField('Taxa de conversão', max_digits=8, decimal_places=3, blank=True, null=True)
    fatura = models.ForeignKey(Fatura, on_delete=models.CASCADE, related_name='gastos_viagem', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.moeda:
            # Set REAL as default
            self.moeda = Moeda.objects.filter(sigla='BRL').first()
        super(GastoViagem, self).save(*args, **kwargs)

    def __str__(self):
        return self.descricao
