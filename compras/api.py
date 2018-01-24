from compras import models
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated


class MercadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mercado
        fields = '__all__'


class SecaoListaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SecaoLista
        fields = '__all__'


class ItensListaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ItensLista
        fields = '__all__'


class ItemCompraSerialier(serializers.ModelSerializer):
    class Meta:
        model = models.ItemCompra
        fields = '__all__'


class MercadoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = models.Mercado.objects.all()
    serializer_class = MercadoSerializer


class SecaoListaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = models.SecaoLista.objects.all()
    serializer_class = SecaoListaSerializer


class ItensListaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = models.ItensLista.objects.all()
    serializer_class = ItensListaSerializer


class ItemCompraViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = models.ItemCompra.objects.all()
    serializer_class = ItemCompraSerialier
