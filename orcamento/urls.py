import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.OrcamentoAtual.as_view(), name='orcamento_atual'),
    url(r'^(?P<ano>[0-9]+)/(?P<mes>[0-9]+)', views.OrcamentoView.as_view(), name='orcamento'),
    url(r'^estatisticas/', views.EstatisticaView.as_view(), name='estatistica'),
    url(r'^ajustar-categorias/', views.AjustarCategoriasView.as_view(), name='ajustar-categorias'),
]
