from django.contrib import admin
from cartao import models


class CartaoAliasSMSInline(admin.TabularInline):
    extra = 0
    model = models.CartaoAliasSMS


@admin.register(models.Bandeira)
class BandeiraAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Cartao)
class CartaoAdmin(admin.ModelAdmin):
    inlines = [CartaoAliasSMSInline]


class CompraCartaoInline(admin.TabularInline):
    extra = 0
    model = models.CompraCartao


@admin.register(models.Fatura)
class FaturaAdmin(admin.ModelAdmin):
    inlines = [CompraCartaoInline]
    list_display = ['__str__', 'valor_inicial', 'valor_final', 'aberta']
    list_filter = ['cartao', 'aberta', 'orcamento']
    readonly_fields = ['valor_inicial']


@admin.register(models.SMSCartao)
class SMSCartaoAdmin(admin.ModelAdmin):
    list_display = ['texto', 'criado']
