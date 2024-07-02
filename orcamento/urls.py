from orcamento import views
from django.urls import path

app_name = 'orcamento'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<int:ano>/<int:mes>', views.OrcamentoView.as_view(), name='orcamento'),
    path('orcamentos/', views.OrcamentosView.as_view(), name='orcamentos'),
    path('estatisticas/', views.EstatisticaView.as_view(), name='estatistica'),
    path('ajustar-categorias/', views.AjustarCategoriasView.as_view(), name='ajustar-categorias'),
]
