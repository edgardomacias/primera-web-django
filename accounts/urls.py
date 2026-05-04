from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.PerfilView.as_view(), name='perfil'),
    path('perfil/editar/', views.PerfilEditView.as_view(), name='perfil_editar'),
    path('perfil/password/', views.cambio_password, name='cambio_password'),
]
