from cartao import views
from django.conf.urls import url

urlpatterns = [
    url(r'^novo$', views.CadastrarCompraCartaoView.as_view(), name='cadastrar-compra'),
    url(r'^fechar-fatura$', views.FecharFaturaView.as_view(), name='fechar-fatura'),
]
