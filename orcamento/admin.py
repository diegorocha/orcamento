from django.contrib import admin
from compras.admin import MercadoInline
from orcamento import models


class ContaInline(admin.TabularInline):
    extra = 0
    model = models.Conta


class EnergiaEletricaInline(admin.StackedInline):
    extra = 0
    model = models.EnergiaEletrica


@admin.register(models.Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    pass

    
@admin.register(models.Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_filter = ['ano']
    inlines = [ContaInline, EnergiaEletricaInline, MercadoInline]
    list_display = ['__str__', 'previsto', 'atual', 'a_pagar', 'mercado_principal']


@admin.register(models.Conta)
class ContaAdmin(admin.ModelAdmin):
    list_display = ['orcamento', 'nome', 'descricao', 'categoria', 'previsto', 'atual', 'a_pagar', 'pago', 'situacao', ]
    list_filter = ['orcamento', 'situacao', ]
    actions = ['acertar_situacao', ]

    def acertar_situacao(self, request, queryset):
        for conta in queryset:
            if conta.esta_pago() and conta.situacao != models.Conta.PAGO:
                conta.situacao = models.Conta.PAGO
                conta.save()
