from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'cadastro_hotel'
urlpatterns = [
    path('', views.lista_hotel, name='lista_hotel'),
    path('hotel/<int:pk>/', views.detalhe_hotel, name='detalhe_hotel'),
    path('quarto/<int:pk>/', views.check_in, name='reserva_quarto'),
    path('reserva/<int:pk>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),
    path('registrar_hotel', views.hotel_registrar, name='registrar_hotel'),
    path('reserva/<int:pk>/confirmar_reserva', views.confirmar_reserva, name='confirmar_reserva'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
