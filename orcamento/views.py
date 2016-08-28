import models
import serializers
from datetime import date
from django.http import Http404
from django.views import generic
from rest_framework import viewsets
from rest_framework.response import Response
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import detail_route, list_route


class OrcamentoAtual(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        hoje = date.today()
        return reverse('orcamento:orcamento', kwargs={'ano': hoje.year, 'mes': hoje.month})


class OrcamentoView(LoginRequiredMixin, generic.DetailView):
    template_name = 'orcamento.html'

    def get_object(self, queryset=None):
        return get_object_or_404(models.Orcamento, ano=self.kwargs['ano'], mes=self.kwargs['mes'])


class OrcamentoViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = models.Orcamento.objects.all()
    serializer_class = serializers.OrcamentoSerializer


class ContaViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = models.Conta.objects.all()
    serializer_class = serializers.ContaSerializer

    @list_route()
    def sem_categoria(self, request):
        queryset = self.queryset.filter(categoria__isnull=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @list_route()
    def ajustar(self, request):
        queryset = self.queryset.filter(categoria__isnull=True).first()
        if queryset:
            serializer = self.get_serializer(queryset)
            return Response(serializer.data)
        else:
            raise Http404


class CategoriaViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = models.Categoria.objects.all()
    serializer_class = serializers.CategoriaSerializer


class EstatisticaView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'estatisticas.html'


class AjustarCategoriasView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'ajustar-contas-sem-categoria.html'
