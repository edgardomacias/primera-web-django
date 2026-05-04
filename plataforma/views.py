from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Avg
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy

from .models import Restaurante, Resena, Usuario
from .forms import RestauranteForm, ResenaForm, UsuarioForm, BuscarForm


def index(request):
    return render(request, "plataforma/index.html", {
        "total_restaurantes": Restaurante.objects.count(),
        "total_resenas": Resena.objects.count(),
        "total_usuarios": Usuario.objects.count(),
        "ultimos_restaurantes": Restaurante.objects.all()[:6],
    })


# CBV 1: Listado de restaurantes
class RestaurantesListView(ListView):
    model = Restaurante
    template_name = "plataforma/restaurantes_list.html"
    context_object_name = "restaurantes"
    ordering = ["nombre"]


def restaurante_detail(request, pk):
    restaurante = get_object_or_404(Restaurante, pk=pk)
    resenas = restaurante.resenas.all()
    promedio = resenas.aggregate(Avg("calificacion"))["calificacion__avg"] or 0
    return render(request, "plataforma/restaurante_detail.html", {
        "restaurante": restaurante,
        "resenas": resenas,
        "promedio": round(promedio, 1),
    })


@login_required
def restaurante_crear(request):
    if request.method == "POST":
        form = RestauranteForm(request.POST, request.FILES)
        if form.is_valid():
            restaurante = form.save()
            messages.success(request, f'Restaurante "{restaurante.nombre}" creado exitosamente.')
            return redirect("restaurante_detail", pk=restaurante.pk)
    else:
        form = RestauranteForm()
    return render(request, "plataforma/restaurante_form.html", {"form": form, "titulo": "Nuevo Restaurante"})


# CBV 2: Editar restaurante con LoginRequiredMixin
class RestauranteEditView(LoginRequiredMixin, UpdateView):
    model = Restaurante
    form_class = RestauranteForm
    template_name = "plataforma/restaurante_form.html"

    def get_success_url(self):
        return reverse_lazy("restaurante_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = f"Editar: {self.object.nombre}"
        ctx["editando"] = True
        return ctx

    def form_valid(self, form):
        messages.success(self.request, f'Restaurante "{self.object.nombre}" actualizado.')
        return super().form_valid(form)


# CBV 3: Borrar restaurante con LoginRequiredMixin
class RestauranteDeleteView(LoginRequiredMixin, DeleteView):
    model = Restaurante
    template_name = "plataforma/restaurante_confirm_delete.html"
    success_url = reverse_lazy("restaurantes_list")
    context_object_name = "restaurante"

    def form_valid(self, form):
        messages.success(self.request, f'Restaurante "{self.object.nombre}" eliminado.')
        return super().form_valid(form)


@login_required
def resena_crear(request):
    restaurante_pk = request.GET.get("restaurante")
    initial = {}
    if restaurante_pk:
        initial["restaurante"] = restaurante_pk
    if request.method == "POST":
        form = ResenaForm(request.POST)
        if form.is_valid():
            resena = form.save()
            messages.success(request, "Reseña publicada exitosamente.")
            return redirect("restaurante_detail", pk=resena.restaurante.pk)
    else:
        form = ResenaForm(initial=initial)
    return render(request, "plataforma/resena_form.html", {"form": form, "titulo": "Nueva Reseña"})


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


def about(request):
    return render(request, "plataforma/about.html", {"titulo": "Acerca de Mí"})
