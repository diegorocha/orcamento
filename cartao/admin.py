from django.contrib import admin
from cartao import models


@admin.register(models.Bandeira)
class BandeiraAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Cartao)
class CartaoAdmin(admin.ModelAdmin):
    pass


class CompraCartaoInline(admin.TabularInline):
    extra = 0
    model = models.CompraCartao


@admin.register(models.Fatura)
class FaturaAdmin(admin.ModelAdmin):
    inlines = [CompraCartaoInline]
