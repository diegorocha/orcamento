import models
from rest_framework import serializers


class OrcamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Orcamento


class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Conta
        read_only_fields = ('a_pagar',)