import models
from datetime import date
from django.views import generic
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


class ListaAtualView(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        hoje = date.today()
        return reverse('compras:lista', kwargs={'ano': hoje.year, 'mes': hoje.month})


class ListaView(LoginRequiredMixin, generic.DetailView):
    template_name = 'lista-compras.html'

    def get_object(self, queryset=None):
        return get_object_or_404(models.ListaCompras, orcamento__ano=self.kwargs['ano'], orcamento__mes=self.kwargs['mes'])
