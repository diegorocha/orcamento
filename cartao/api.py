# coding: utf-8
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cartao import models
from cartao.utils import fechar_fatura, parse_sms
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


class CompraCartaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompraCartao
        fields = '__all__'


class CompraCartaoListSerializer(CompraCartaoSerializer):
    categoria = serializers.StringRelatedField()


class CompraCartaoFullSerializer(CompraCartaoListSerializer):
    fatura = FaturaSerializer()


class FaturaRetrieveSerializer(FaturaSerializer):
    compras = CompraCartaoListSerializer(many=True)


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
    serializer_class_retrieve = FaturaRetrieveSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.serializer_class_retrieve
        return self.serializer_class

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

    @list_route()
    def abertas(self, request):
        faturas = self.queryset.filter(aberta=True)
        return Response(self.serializer_class(faturas, many=True).data)

    @list_route()
    def get_by_alias(self, request):
        alias_param = request.query_params.get('alias')
        if not alias_param:
            return Response(status=404)
        alias = models.CartaoAliasSMS.objects.filter(texto__iexact=alias_param).first()
        if not alias:
            return Response(status=404)
        fatura = alias.cartao.faturas.filter(aberta=True).first()
        if not fatura:
            return Response(status=404)
        return Response(self.serializer_class(fatura).data)


class CompraCartaoViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = models.CompraCartao.objects.all().order_by('-id')

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return CompraCartaoSerializer
        return CompraCartaoFullSerializer


class SMSCartaoViewset(viewsets.mixins.CreateModelMixin, viewsets.mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = models.SMSCartao.objects.all()
    serializer_class = SMSCartaoSerializer

    @list_route()
    def proximo(self, request):
        sms = self.queryset.first()
        if not sms:
            return Response(status=404)
        return Response(parse_sms(sms))

    @list_route(methods=['POST'])
    def parse(self, request):
        texto = request.data.get('sms') or request.POST.get('sms')
        if not texto:
            return Response(status=400)
        sms = models.SMSCartao(texto=texto)
        data = parse_sms(sms)
        if not data:
            return Response(status=422)
        return Response(data)
