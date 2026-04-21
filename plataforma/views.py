from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Avg

from .models import Restaurante, Resena, Usuario
from .forms import RestauranteForm, ResenaForm, UsuarioForm, BuscarForm


def index(request):
    return render(request, "plataforma/index.html", {
        "total_restaurantes": Restaurante.objects.count(),
        "total_resenas": Resena.objects.count(),
        "total_usuarios": Usuario.objects.count(),
        "ultimos_restaurantes": Restaurante.objects.all()[:6],
    })


def restaurantes_list(request):
    restaurantes = Restaurante.objects.all()
    return render(request, "plataforma/restaurantes_list.html", {"restaurantes": restaurantes})


def restaurante_detail(request, pk):
    restaurante = get_object_or_404(Restaurante, pk=pk)
    resenas = restaurante.resenas.all()
    promedio = resenas.aggregate(Avg("calificacion"))["calificacion__avg"] or 0
    return render(request, "plataforma/restaurante_detail.html", {
        "restaurante": restaurante,
        "resenas": resenas,
        "promedio": round(promedio, 1),
    })


def restaurante_crear(request):
    if request.method == "POST":
        form = RestauranteForm(request.POST)
        if form.is_valid():
            restaurante = form.save()
            return redirect("restaurante_detail", pk=restaurante.pk)
    else:
        form = RestauranteForm()
    return render(request, "plataforma/restaurante_form.html", {"form": form, "titulo": "Nuevo Restaurante"})


def resena_crear(request):
    if request.method == "POST":
        form = ResenaForm(request.POST)
        if form.is_valid():
            resena = form.save()
            return redirect("restaurante_detail", pk=resena.restaurante.pk)
    else:
        form = ResenaForm()
    return render(request, "plataforma/resena_form.html", {"form": form, "titulo": "Nueva Resena"})


def usuario_crear(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = UsuarioForm()
    return render(request, "plataforma/usuario_form.html", {"form": form, "titulo": "Nuevo Usuario"})


def buscar(request):
    form = BuscarForm(request.GET)
    restaurantes = None
    query = ""
    if form.is_valid():
        query = form.cleaned_data.get("query", "")
        if query:
            restaurantes = Restaurante.objects.filter(
                Q(nombre__icontains=query) | Q(tipo_cocina__icontains=query) | Q(ciudad__icontains=query)
            )
        else:
            restaurantes = Restaurante.objects.none()
    return render(request, "plataforma/buscar.html", {"form": form, "restaurantes": restaurantes, "query": query})
