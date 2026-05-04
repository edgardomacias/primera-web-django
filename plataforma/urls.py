from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("restaurantes/", views.RestaurantesListView.as_view(), name="restaurantes_list"),
    path("restaurantes/nuevo/", views.restaurante_crear, name="restaurante_crear"),
    path("restaurantes/<int:pk>/", views.restaurante_detail, name="restaurante_detail"),
    path("restaurantes/<int:pk>/editar/", views.RestauranteEditView.as_view(), name="restaurante_editar"),
    path("restaurantes/<int:pk>/borrar/", views.RestauranteDeleteView.as_view(), name="restaurante_borrar"),
    path("resenas/nueva/", views.resena_crear, name="resena_crear"),
    path("usuarios/nuevo/", views.usuario_crear, name="usuario_crear"),
    path("buscar/", views.buscar, name="buscar"),
]
