from viagem import views
from django.urls import path

app_name = 'viagem'
urlpatterns = [
    path('<int:viagem_id>', views.ViagemView.as_view(), name='viagem'),
]
