from compras import views
from django.urls import path

app_name = 'compras'
urlpatterns = [
    path('', views.ListaAtualView.as_view(), name='lista-atual'),
    path('listas', views.ListaComprasView.as_view(), name='listas'),
    path('<int:ano>/<int:mes>', views.ListaView.as_view(), name='lista'),
]
