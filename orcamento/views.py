import models
import serializers
from django.views import generic
from rest_framework import viewsets
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404


class OrcamentoAtual(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('orcamento:orcamento', kwargs={'ano': 2016, 'mes': 7})


class OrcamentoView(generic.DetailView):
    template_name = 'orcamento.html'

    def get_object(self, queryset=None):
        return get_object_or_404(models.Orcamento, ano=self.kwargs['ano'], mes=self.kwargs['mes'])


class OrcamentoViewSet(viewsets.ModelViewSet):
    queryset = models.Orcamento.objects.all()
    serializer_class = serializers.OrcamentoSerializer


class ContaViewSet(viewsets.ModelViewSet):
    queryset = models.Conta.objects.all()
    serializer_class = serializers.ContaSerializer
