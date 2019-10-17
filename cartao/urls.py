from cartao import views
from django.conf.urls import url

app_name = 'cartao'
urlpatterns = [
    url(r'(?P<cartao_id>[0-9]+)/faturas/$', views.ProximasFaturasView.as_view(), name='proximas-faturas'),
    url(r'fatura/(?P<fatura_id>[0-9]+)$', views.FaturaView.as_view(), name='fatura'),
    url(r'^novo$', views.CadastrarCompraCartaoView.as_view(), name='cadastrar-compra'),
    url(r'^fechar-fatura$', views.FecharFaturaView.as_view(), name='fechar-fatura'),
    url(r'^sms$', views.SMSView.as_view(), name='sms'),
    url(r'^renata$', views.CartaoRenataView.as_view(), name='cartao-renata'),
]
