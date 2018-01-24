from cartao import views
from django.conf.urls import url

app_name = 'cartao'
urlpatterns = [
    url(r'fatura/(?P<fatura_id>[0-9]+)$', views.FaturaView.as_view(), name='fatura'),
    url(r'^novo$', views.CadastrarCompraCartaoView.as_view(), name='cadastrar-compra'),
    url(r'^fechar-fatura$', views.FecharFaturaView.as_view(), name='fechar-fatura'),
]
