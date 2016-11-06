from django.contrib import admin
import models


class MercadoInline(admin.TabularInline):
    extra = 0
    model = models.Mercado


class ItemCompraInline(admin.TabularInline):
    extra = 0
    model = models.ItemCompra


@admin.register(models.Mercado)
class MercadoAdmin(admin.ModelAdmin):
    pass


@admin.register(models.SecaoLista)
class SecaoListaAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ItensLista)
class ItensListaAdmin(admin.ModelAdmin):
    list_filter = ['secao']


@admin.register(models.ListaCompras)
class ListaComprasAdmin(admin.ModelAdmin):
    inlines = (ItemCompraInline, )
