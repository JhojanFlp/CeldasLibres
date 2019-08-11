from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib import messages
from bootstrap_modal_forms.generic import BSModalCreateView

# Create your views here.

from .models import Vehiculo , VehiculoClienteFrecuente
from .forms import CrearVehiculoForm, CrearVehiculoClienteFrecuenteForm
from parqueaderos import views

@method_decorator([login_required, staff_member_required], name='dispatch')
class CrearVehiculo(BSModalCreateView):
    model = Vehiculo
    template_name = 'vehiculos/crear_vehiculo.html'
    form_class = CrearVehiculoForm
    success_url = reverse_lazy('crear-tarifa')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        anno = request.POST.get('anno')
        tipo_vehiculo = request.POST.get('tipo_vehiculo')
        if form.is_valid():
            messages.success(request, 'Vehiculo creado')
        return super(CrearVehiculo, self).post(request, *args, **kwargs)

@method_decorator([login_required, staff_member_required], name='dispatch')
class VerVehiculos(ListView):
    model = Vehiculo
    context_object_name = 'vehiculos_list'
    template_name = 'vehiculos/vehiculos.html'

@method_decorator([login_required, staff_member_required], name='dispatch')
class ModificarVehiculo(UpdateView):
    model = Vehiculo
    form_class = CrearVehiculoForm
    template_name_suffix = '_update_form'
    success_url =  reverse_lazy('crear-parqueadero')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        messages.success(request, 'Vehiculo modificado')
        return super(ModificarVehiculo, self).post(request, kwargs)

@method_decorator([login_required, staff_member_required], name='dispatch')
class EliminarVehiculo(DeleteView):
    model = Vehiculo
    form_class = CrearVehiculoForm
    success_url = reverse_lazy('vehiculos')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        messages.success(request, 'Vehiculo eliminado')
        return super(EliminarVehiculo, self).post(request, kwargs)


@method_decorator([login_required], name='dispatch')
class CrearVehiculoClienteFrecuente(CreateView):
    model = VehiculoClienteFrecuente
    template_name = 'vehiculos/crear_vehiculo_cliente.html'
    form_class = CrearVehiculoClienteFrecuenteForm
    success_url = reverse_lazy('vehiculos-clientes')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            messages.success(request, 'Vehiculo de cliente frecuente creado correctamente')
        return super(CrearVehiculoClienteFrecuente, self).post(request, *args, **kwargs)


@method_decorator([login_required], name='dispatch')
class VerVehiculosClientes(ListView):
    model = VehiculoClienteFrecuente
    context_object_name = 'vehiculos_list'
    template_name = 'vehiculos/vehiculos_clientes.html'


@method_decorator([login_required], name='dispatch')
class EliminarVehiculoCliente(DeleteView):
    model = VehiculoClienteFrecuente
    form_class = CrearVehiculoClienteFrecuenteForm
    success_url = reverse_lazy('vehiculos-clientes')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        messages.success(request, 'Vehiculo eliminado correctamente')
        return super(EliminarVehiculoCliente, self).post(request, *args, **kwargs)


@method_decorator([login_required], name='dispatch')
class ModificarVehiculoCliente(UpdateView):
    model = VehiculoClienteFrecuente
    form_class = CrearVehiculoClienteFrecuenteForm
    template_name_suffix = '_update_form'
    success_url =  reverse_lazy('vehiculos-clientes')

    def post(self, request, *args, **kwargs):
        request.POST = request.POST.copy()
        form = self.form_class(request.POST)
        if form.is_valid():
            messages.success(request, 'Vehiculo actualizado correctamente')
        return super(ModificarVehiculoCliente, self).post(request, *args, **kwargs)
       