from compras import views
from django.conf.urls import url

app_name = 'compras'
urlpatterns = [
    url(r'^$', views.ListaAtualView.as_view(), name='lista-atual'),
    url(r'^listas$', views.ListaComprasView.as_view(), name='listas'),
    url(r'^(?P<ano>[0-9]+)/(?P<mes>[0-9]+)', views.ListaView.as_view(), name='lista'),
]
