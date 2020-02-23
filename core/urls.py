from django.contrib import admin
from rest_framework import routers
from cartao import api as api_cartao
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
router.register(r'cartao/bandeira', api_cartao.BandeiraViewset)
router.register(r'cartao/cartao', api_cartao.CartaoViewset)
router.register(r'cartao/fatura', api_cartao.FaturaViewset)
router.register(r'cartao/compra', api_cartao.CompraCartaoViewset)
router.register(r'cartao/sms', api_cartao.SMSCartaoViewset)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include((router.urls, 'api'), namespace='api')),
    url(r'^compras/', include('compras.urls', namespace='compras')),
    url(r'^cartao/', include('cartao.urls', namespace='cartao')),
    url(r'^viagem/', include('viagem.urls', namespace='viagem')),
    url(r'', include('orcamento.urls', namespace='orcamento')),
]
