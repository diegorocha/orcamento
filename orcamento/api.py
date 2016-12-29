import utils
import models
from django.http import Http404
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route, list_route


class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Conta
        read_only_fields = ('a_pagar',)


class OrcamentoSerializer(serializers.ModelSerializer):
    contas = ContaSerializer(many=True, read_only=True)

    class Meta:
        model = models.Orcamento


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Categoria


class OrcamentoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = models.Orcamento.objects.all()
    serializer_class = OrcamentoSerializer

    @list_route()
    def estatisticas(self, request):
        return Response(utils.gerar_estatisticas())

    @list_route()
    def mercado(self, request):
        return Response(utils.estatisticas_mercado())

    @list_route()
    def total(self, request):
        return Response(utils.estatisticas_total())

    @detail_route()
    def estatistica(self, request, pk):
        orcamento = get_object_or_404(self.queryset, pk=pk)
        return Response(utils.estatisticas_orcamento(orcamento))


class ContaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = models.Conta.objects.all()
    serializer_class = ContaSerializer

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


class CategoriaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = models.Categoria.objects.all()
    serializer_class = CategoriaSerializer
