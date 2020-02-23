from django.contrib import admin

from viagem import models


class GastoViagemInline(admin.TabularInline):
    extra = 0
    model = models.GastoViagem


@admin.register(models.Viagem)
class OrcamentoAdmin(admin.ModelAdmin):
    list_filter = ['orcamento']
    list_display = ['__str__', 'inicio', 'fim', 'custo_total']
    inlines = [GastoViagemInline, ]
