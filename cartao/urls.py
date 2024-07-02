from cartao import views
from django.urls import path

app_name = 'cartao'
urlpatterns = [
    path('<int:cartao_id>/faturas/', views.ProximasFaturasView.as_view(), name='proximas-faturas'),
    path('fatura/<int:fatura_id>', views.FaturaView.as_view(), name='fatura'),
    path('novo', views.CadastrarCompraCartaoView.as_view(), name='cadastrar-compra'),
    path('fechar-fatura', views.FecharFaturaView.as_view(), name='fechar-fatura'),
    path('sms', views.SMSView.as_view(), name='sms'),
    path('terceiros', views.CartaoTerceirosView.as_view(), name='cartao-terceiros'),
    path('terceiros/download', views.CartaoTerceirosDownloadView.as_view(), name='carta-terceiros-download'),
]
