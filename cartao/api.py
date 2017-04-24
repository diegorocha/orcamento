from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from cartao import models


class BandeiraSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bandeira


class CartaoSerializer(serializers.ModelSerializer):
    bandeira = serializers.StringRelatedField()
    class Meta:
        model = models.Cartao


class FaturaSerializer(serializers.ModelSerializer):
    orcamento = serializers.StringRelatedField()
    cartao = serializers.StringRelatedField()
    valor_inicial = serializers.FloatField(read_only=True)
    class Meta:
        model = models.Fatura


class FaturaRetrieveSerializer(FaturaSerializer):
    cartao = CartaoSerializer()


class CompraCartaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompraCartao


class CompraCartaoFullSerializer(CompraCartaoSerializer):
    fatura = FaturaSerializer()
    class Meta:
        model = models.CompraCartao


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


class CompraCartaoViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = models.CompraCartao.objects.all().order_by('-id')

    def get_serializer_class(self):
        if self.action == "create":
            return CompraCartaoSerializer
        return CompraCartaoFullSerializer
