import views
from django.conf.urls import url, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'conta', views.ContaViewSet)
router.register(r'orcamento', views.OrcamentoViewSet)
router.register(r'categoria', views.CategoriaViewSet)

urlpatterns = [
    url(r'^$', views.OrcamentoAtual.as_view(), name='orcamento_atual'),
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^(?P<ano>[0-9]+)/(?P<mes>[0-9]+)', views.OrcamentoView.as_view(), name='orcamento'),
    url(r'^estatisticas/', views.EstatisticaView.as_view(), name='estatistica'),
    url(r'^ajustar-categorias/', views.AjustarCategoriasView.as_view(), name='ajustar-categorias'),
]
