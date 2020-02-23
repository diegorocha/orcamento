from django.contrib import admin

from viagem import models


@admin.register(models.Viagem)
class OrcamentoAdmin(admin.ModelAdmin):
    list_filter = ['orcamento']
    list_display = ['__str__', 'inicio', 'fim']
