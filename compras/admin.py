from django.contrib import admin
from compras import models


class MercadoInline(admin.TabularInline):
    extra = 0
    model = models.Mercado


class ItemCompraInline(admin.TabularInline):
    extra = 0
    model = models.ItemCompra


@admin.register(models.Mercado)
class MercadoAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'tipo', 'valor']


@admin.register(models.SecaoLista)
class SecaoListaAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ItensLista)
class ItensListaAdmin(admin.ModelAdmin):
    list_filter = ['secao']


@admin.register(models.ListaCompras)
class ListaComprasAdmin(admin.ModelAdmin):
    inlines = (ItemCompraInline, )
