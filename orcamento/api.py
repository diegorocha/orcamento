from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orcamento import models
from orcamento import utils


class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Conta
        fields = '__all__'
        read_only_fields = ('a_pagar',)


class OrcamentoSerializer(serializers.ModelSerializer):
    contas = ContaSerializer(many=True, read_only=True)

    class Meta:
        model = models.Orcamento
        fields = '__all__'


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Categoria
        fields = '__all__'


class OrcamentoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = models.Orcamento.objects.all()
    serializer_class = OrcamentoSerializer

    @action(detail=False)
    def estatisticas(self, request):
        return Response(utils.gerar_estatisticas())

    @action(detail=False)
    def mercado(self, request):
        return Response(utils.estatisticas_mercado())

    @action(detail=False)
    def energia_eletrica(self, request):
        return Response(utils.estatisticas_energia_eletrica())

    @action(detail=False)
    def total(self, request):
        return Response(utils.estatisticas_total())

    @action(detail=True)
    def estatistica(self, request, pk):
        orcamento = get_object_or_404(self.queryset, pk=pk)
        return Response(utils.estatisticas_orcamento(orcamento))


class ContaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = models.Conta.objects.all()
    serializer_class = ContaSerializer

    @action(detail=False)
    def sem_categoria(self, request):
        queryset = self.queryset.filter(categoria__isnull=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False)
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
