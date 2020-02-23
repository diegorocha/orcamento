from viagem import views
from django.conf.urls import url

app_name = 'viagem'
urlpatterns = [
    url(r'(?P<viagem_id>[0-9]+)$', views.ViagemView.as_view(), name='viagem'),
]
