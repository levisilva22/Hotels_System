from django.urls import path
from . import views

app_name = "hotels"
urlpatterns = [
    path("", views.hotel_list, name="hotels_list"),
    path("hotel/<int:pk>/", views.hotel_detail, name="hotel_detail"),
    path("quarto/<int:quarto_id>/reserva/", views.reserva_quarto, name="reserva_quarto"),
    path("quarto/<int:reserva_id>/cancelar/", views.cancelar_reserva, name="cancelar_reserva"),
]
