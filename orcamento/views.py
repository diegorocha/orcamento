from orcamento import models
from datetime import date
from django.views import generic
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from core.views import BaseViewMixin


class HomeView(BaseViewMixin, generic.TemplateView):
    template_name = 'home.html'

    def get_redirect_url(self, *args, **kwargs):
        hoje = date.today()
        return reverse('orcamento:orcamento', kwargs={'ano': hoje.year, 'mes': hoje.month})

    def get(self, request, *args, **kwargs):
        if request.user.has_perm('orcamento.change_orcamento'):
            return redirect(self.get_redirect_url(*args, **kwargs))
        return super(HomeView, self).get(self, request, *args, **kwargs)


class OrcamentoView(BaseViewMixin, generic.DetailView):
    template_name = 'orcamento.html'
    permission_required = 'orcamento.change_orcamento'

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
