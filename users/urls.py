from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('login/<int:pk>/perfil', views.perfil, name='perfil'),

]
