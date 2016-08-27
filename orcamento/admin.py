from django.contrib import admin
import models


class ContaInline(admin.TabularInline):
    model = models.Conta


@admin.register(models.Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    inlines = [ContaInline]


@admin.register(models.Conta)
class ContaAdmin(admin.ModelAdmin):
    list_display = ['orcamento', 'nome', 'descricao', 'previsto', 'atual', 'a_pagar', 'pago', 'situacao', ]
    list_filter = ['orcamento', 'situacao', ]
    actions = ['acertar_situacao', ]

    def acertar_situacao(self, request, queryset):
        for conta in queryset:
            if conta.esta_pago() and conta.situacao != models.Conta.PAGO:
                conta.situacao = models.Conta.PAGO
                conta.save()
