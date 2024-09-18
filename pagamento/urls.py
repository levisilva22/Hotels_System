from django.urls import path
from . import views

app_name = 'pagamento'

urlpatterns = [
    path('adicionar_cartaocredit/', views.cartaocredit_add, name='add_cartaocredito'),
    path('adicionar_cartaodebito', views.cartaodebit_add, name='add_cartaodebito'),
    path('metodo_de_pagamento/<int:reserva_id>/', views.validar_pagamento, name='pagamento'),
]
