from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from orcamento.models import Orcamento


@python_2_unicode_compatible
class Viagem(models.Model):
    class Meta:
        verbose_name = 'Viagem'
        verbose_name_plural = 'Viagens'
        ordering = ['-inicio', '-fim']
    descricao = models.CharField('Descrição', max_length=50, blank=False, null=False)
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name='viagens')
    inicio = models.DateField('Início', blank=False)
    fim = models.DateField('Fim', blank=False)

    def __str__(self):
        return self.descricao + self.inicio.strftime(' %Y/%m')
