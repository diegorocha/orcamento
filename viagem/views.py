from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.views import generic

from core.views import BaseViewMixin
from viagem import models


class ViagemView(BaseViewMixin, generic.TemplateView):
    template_name = 'viagem.html'
    viagem = None

    def get_object(self):
        self.viagem = get_object_or_404(models.Viagem, id=self.kwargs['viagem_id'])

    def get_gastos_por_dia(self):
        dias = self.viagem.gastos.values('dia').annotate(total=Sum('valor_real'))
        for dia in dias:
            dia['gastos'] = self.viagem.gastos.filter(dia=dia['dia'])
        return dias

    def get_gastos_por_categoria(self):
        return self.viagem.gastos.values('categoria__descricao').annotate(total=Sum('valor_real')).order_by('-total')

    def get_context_data(self, **kwargs):
        self.get_object()
        data = super(ViagemView, self).get_context_data(**kwargs)
        data['viagem'] = self.viagem
        data['dias'] = self.get_gastos_por_dia()
        data['categorias'] = self.get_gastos_por_categoria()
        return data
