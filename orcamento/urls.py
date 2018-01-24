from orcamento import views
from django.conf.urls import url

app_name = 'orcamento'
urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^(?P<ano>[0-9]+)/(?P<mes>[0-9]+)', views.OrcamentoView.as_view(), name='orcamento'),
    url(r'^orcamentos/', views.OrcamentosView.as_view(), name='orcamentos'),
    url(r'^estatisticas/', views.EstatisticaView.as_view(), name='estatistica'),
    url(r'^ajustar-categorias/', views.AjustarCategoriasView.as_view(), name='ajustar-categorias'),
]
