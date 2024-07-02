from django.contrib import admin
from rest_framework import routers
from cartao import api as api_cartao
from compras import api as api_compras
from core.views import HealthCheckView
from orcamento import api as api_orcamento
from django.urls import path, include
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
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include((router.urls, 'api'), namespace='api')),
    path('compras/', include('compras.urls', namespace='compras')),
    path('cartao/', include('cartao.urls', namespace='cartao')),
    path('viagem/', include('viagem.urls', namespace='viagem')),
    path('', include('orcamento.urls', namespace='orcamento')),
    path('healthcheck/', HealthCheckView.as_view(), name='healthcheck'),
]
