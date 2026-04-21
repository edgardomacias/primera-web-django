from django import forms
from .models import Restaurante, Resena, Usuario


class RestauranteForm(forms.ModelForm):
    class Meta:
        model = Restaurante
        fields = ["nombre", "direccion", "tipo_cocina", "telefono", "ciudad"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del restaurante"}),
            "direccion": forms.TextInput(attrs={"class": "form-control", "placeholder": "Dirección completa"}),
            "tipo_cocina": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: Italiana, Japonesa, Peruana"}),
            "telefono": forms.TextInput(attrs={"class": "form-control", "placeholder": "+56 9 XXXX XXXX"}),
            "ciudad": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ciudad"}),
        }


class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ["restaurante", "calificacion", "comentario"]
        widgets = {
            "restaurante": forms.Select(attrs={"class": "form-select"}),
            "calificacion": forms.Select(attrs={"class": "form-select"}),
            "comentario": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "placeholder": "Cuéntanos tu experiencia..."}
            ),
        }


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["nombre", "email", "resena"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Tu nombre completo"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "correo@ejemplo.com"}),
            "resena": forms.Select(attrs={"class": "form-select"}),
        }


class BuscarForm(forms.Form):
    query = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control form-control-lg", "placeholder": "Buscar por nombre, tipo de cocina o ciudad..."}
        ),
    )
