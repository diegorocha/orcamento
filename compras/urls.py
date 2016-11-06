import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.ListaAtualView.as_view(), name='lista-atual'),
    url(r'^(?P<ano>[0-9]+)/(?P<mes>[0-9]+)', views.ListaView.as_view(), name='lista'),
]
