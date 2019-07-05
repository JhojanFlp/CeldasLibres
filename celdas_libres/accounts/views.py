from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import SignUpForm, UpdateUsuarioForm
from .models import CustomUser, Usuario
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib import messages


@method_decorator([login_required, staff_member_required], name='dispatch')
class CrearUsuario(CreateView):
    template_name = 'accounts/signup.html'
    model = CustomUser
    form_class = SignUpForm
    success_url =  reverse_lazy('home')


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password1')
            user = form.save()
            user.usuario.identificacion = form.cleaned_data['username']
            user.usuario.tipo_identificacion = form.cleaned_data['tipo_identificacion']
            user.usuario.nacionalidad = form.cleaned_data['nacionalidad']
            user.usuario.fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
            user.usuario.telefono = form.cleaned_data['telefono']
            user.usuario.celular = form.cleaned_data['celular']
            user.usuario.direccion = form.cleaned_data['direccion']
            user.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

            messages.success(request, 'Usuario registrado correctamente')
            return redirect('home')
        return render(request, 'accounts/signup.html', {'form': form})

@method_decorator([login_required, staff_member_required], name='dispatch')
class ModificarUsuario(UpdateView):
    model = Usuario
    form_class = UpdateUsuarioForm
    template_name_suffix = '_update_form'
    success_url =  reverse_lazy('usuarios')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            messages.success(request, 'Usuario actualizado correctamente')
        return super(ModificarUsuario, self).post(request, kwargs)

@method_decorator([login_required, staff_member_required], name='dispatch')
class VerUsuarios(ListView):
    model = Usuario
    context_object_name = 'usuarios_list'
    template_name = 'accounts/usuarios_list.html'

@method_decorator([login_required, staff_member_required], name='dispatch')
class EliminarUsuario(DeleteView):
    model = Usuario
    success_url = reverse_lazy('usuarios')

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Usuario elinimado correctamente')
        return super(EliminarUsuario, self).post(request, *args, **kwargs)
