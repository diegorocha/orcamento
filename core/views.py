from django.contrib.auth.mixins import LoginRequiredMixin

from compras.models import ListaCompras
from orcamento.models import Orcamento


class UltimosOrcamentosMixin(object):
    def get_context_data(self, **kwargs):
        context = super(UltimosOrcamentosMixin, self).get_context_data(**kwargs)
        context['ultimos_orcamentos'] = Orcamento.objects.all()[:6]
        return context


class UltimasListasMixin(object):
    def get_context_data(self, **kwargs):
        context = super(UltimasListasMixin, self).get_context_data(**kwargs)
        context['ultimas_listas'] = ListaCompras.objects.all()[:6]
        return context


class BaseViewMixin(LoginRequiredMixin, UltimosOrcamentosMixin, UltimasListasMixin):
    pass


