from orcamento import models
from datetime import date
from django.views import generic
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from core.views import BaseViewMixin
from orcamento.utils import get_contas_url


class HomeView(BaseViewMixin, generic.TemplateView):
    template_name = 'home.html'

    def get_redirect_url(self, *args, **kwargs):
        default = models.OrcamentoDefault.objects.first()
        if default:
            ano = default.orcamento.ano
            mes = default.orcamento.mes
        else:
            hoje = date.today()
            ano = hoje.year
            mes = hoje.month
        return reverse('orcamento:orcamento', kwargs={'ano': ano, 'mes': mes})

    def get(self, request, *args, **kwargs):
        if request.user.has_perm('orcamento.change_orcamento'):
            return redirect(self.get_redirect_url(*args, **kwargs))
        return super(HomeView, self).get(self, request, *args, **kwargs)


class OrcamentoView(BaseViewMixin, generic.DetailView):
    template_name = 'orcamento.html'
    permission_required = 'orcamento.change_orcamento'

    def get_context_data(self, **kwargs):
        context = super(OrcamentoView, self).get_context_data(**kwargs)
        context['contas'] = {
            'url': get_contas_url(context['object'], self.request.user)
        }
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(models.Orcamento, ano=self.kwargs['ano'], mes=self.kwargs['mes'])


class EstatisticaView(BaseViewMixin, generic.TemplateView):
    template_name = 'estatisticas.html'
    permission_required = 'orcamento.change_orcamento'


class AjustarCategoriasView(BaseViewMixin, generic.TemplateView):
    template_name = 'ajustar-contas-sem-categoria.html'
    permission_required = 'orcamento.change_orcamento'


class OrcamentosView(BaseViewMixin, generic.TemplateView):
    template_name = 'lista-orcamentos.html'
    permission_required = 'orcamento.change_orcamento'

    def get_context_data(self, **kwargs):
        context = super(OrcamentosView, self).get_context_data(**kwargs)
        context['itens'] = models.Orcamento.objects.all()
        return context
