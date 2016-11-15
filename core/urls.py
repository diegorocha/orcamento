from django.contrib import admin
from rest_framework import routers
from compras import api as api_compras
from orcamento import api as api_orcamento
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views


router = routers.DefaultRouter()
router.register(r'conta', api_orcamento.ContaViewSet)
router.register(r'orcamento', api_orcamento.OrcamentoViewSet)
router.register(r'categoria', api_orcamento.CategoriaViewSet)
router.register(r'compras/mercado', api_compras.MercadoViewSet)
router.register(r'compras/secao', api_compras.SecaoListaViewSet)
router.register(r'compras/itens', api_compras.ItensListaViewSet)
router.register(r'compras/itens-compra', api_compras.ItemCompraViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^compras/', include('compras.urls', namespace='compras')),
    url(r'', include('orcamento.urls', namespace='orcamento')),
]
