from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("restaurantes/", views.restaurantes_list, name="restaurantes_list"),
    path("restaurantes/nuevo/", views.restaurante_crear, name="restaurante_crear"),
    path("restaurantes/<int:pk>/", views.restaurante_detail, name="restaurante_detail"),
    path("resenas/nueva/", views.resena_crear, name="resena_crear"),
    path("usuarios/nuevo/", views.usuario_crear, name="usuario_crear"),
    path("buscar/", views.buscar, name="buscar"),
]
