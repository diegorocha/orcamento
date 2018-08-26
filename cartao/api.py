# coding: utf-8
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cartao import models
from cartao.utils import fechar_fatura
from orcamento.models import Orcamento


class BandeiraSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bandeira
        fields = '__all__'


class CartaoSerializer(serializers.ModelSerializer):
    bandeira = serializers.StringRelatedField()

    class Meta:
        model = models.Cartao
        fields = '__all__'


class FaturaSerializer(serializers.ModelSerializer):
    orcamento = serializers.StringRelatedField()
    cartao = serializers.StringRelatedField()
    valor_inicial = serializers.FloatField(read_only=True)

    class Meta:
        model = models.Fatura
        fields = '__all__'


class FaturaRetrieveSerializer(FaturaSerializer):
    cartao = CartaoSerializer()


class CompraCartaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompraCartao
        fields = '__all__'


class CompraCartaoFullSerializer(CompraCartaoSerializer):
    fatura = FaturaSerializer()

    class Meta:
        model = models.CompraCartao
        fields = '__all__'


class SMSCartaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SMSCartao
        fields = '__all__'


class BandeiraViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = models.Bandeira.objects.all()
    serializer_class = BandeiraSerializer


class CartaoViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = models.Cartao.objects.all()
    serializer_class = CartaoSerializer


class FaturaViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = models.Fatura.objects.all().order_by('orcamento', 'cartao')
    serializer_class = FaturaSerializer

    @detail_route(methods=['post'])
    def fechar(self, request, pk=None):
        fatura = get_object_or_404(self.queryset, pk=pk)
        valor_final = request.POST.get('valor_final')
        orcamento = Orcamento.objects.filter(pk=request.data.get('orcamento')).first()
        if not orcamento:
            raise ValidationError('Orçamento não encontrado')
        try:
            return Response(self.serializer_class(fechar_fatura(fatura, orcamento, valor_final)).data)
        except Exception as ex:
            return Response(dict(error=str(ex)))


class CompraCartaoViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = models.CompraCartao.objects.all().order_by('-id')

    def get_serializer_class(self):
        if self.action == "create":
            return CompraCartaoSerializer
        return CompraCartaoFullSerializer


class SMSCartaoViewset(viewsets.mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = models.SMSCartao.objects.all()
    serializer_class = SMSCartaoSerializer
