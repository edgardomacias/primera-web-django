from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy

from .forms import RegistroForm, LoginForm, ProfileForm, CambioPasswordForm
from .models import Profile


def registro(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}! Tu cuenta fue creada exitosamente.')
            return redirect('index')
    else:
        form = RegistroForm()
    return render(request, 'accounts/registro.html', {'form': form, 'titulo': 'Crear Cuenta'})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'¡Bienvenido de vuelta, {user.username}!')
            return redirect(request.GET.get('next', 'index'))
    else:
        form = LoginForm(request)
    return render(request, 'accounts/login.html', {'form': form, 'titulo': 'Iniciar Sesión'})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect('index')


class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/perfil.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Mi Perfil'
        return ctx


class PerfilEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/perfil_editar.html'
    success_url = reverse_lazy('perfil')

    def get_object(self):
        return self.request.user.profile

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['first_name'].initial = self.request.user.first_name
        form.fields['last_name'].initial = self.request.user.last_name
        form.fields['email'].initial = self.request.user.email
        return form

    def form_valid(self, form):
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.save()
        messages.success(self.request, 'Perfil actualizado correctamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Editar Perfil'
        return ctx


@login_required
def cambio_password(request):
    if request.method == 'POST':
        form = CambioPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Contraseña cambiada exitosamente.')
            return redirect('perfil')
    else:
        form = CambioPasswordForm(request.user)
    return render(request, 'accounts/cambio_password.html', {'form': form, 'titulo': 'Cambiar Contraseña'})
