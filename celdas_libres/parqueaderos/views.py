from datetime import datetime

from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from .models import Tarifa, EntradaVehiculo
from .forms import CrearTarifaForm, EntradaVehiculoForm
from django.contrib import messages

import re
import time


@method_decorator([login_required, staff_member_required], name='dispatch')
class CrearTarifa(CreateView):
    model = Tarifa
    template_name = 'parqueaderos/crear_tarifa.html'
    form_class = CrearTarifaForm
    success_url = reverse_lazy('tarifas')


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        anno = time.strftime("%Y")
        tipo_vehiculo = request.POST.get('tipo_vehiculo')
        for tarifa in Tarifa.objects.all():
            if (tarifa.anno, tarifa.tipo_vehiculo) == (int(anno), tipo_vehiculo):
                tarifa.delete()
        if form.is_valid():
            messages.success(request, 'Tarifa creada correctamente')
        return super(CrearTarifa, self).post(request, *args, **kwargs)

@method_decorator([login_required], name='dispatch')
class VerTarifas(ListView):
    model = Tarifa
    context_object_name = 'tarifas_list'
    template_name = 'parqueaderos/tarifas.html'

@method_decorator([login_required, staff_member_required], name='dispatch')
class ModificarTarifa(UpdateView):
    model = Tarifa
    form_class = CrearTarifaForm
    template_name_suffix = '_update_form'
    success_url =  reverse_lazy('tarifas')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            messages.success(request, 'Tarifa actualizada correctamente')
        return super(ModificarTarifa, self).post(request, *args, **kwargs)

@method_decorator([login_required, staff_member_required], name='dispatch')
class EliminarTarifa(DeleteView):
    model = Tarifa
    form_class = CrearTarifaForm
    success_url = reverse_lazy('tarifas')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            messages.success(request, 'Tarifa eliminada correctamente')
        return super(EliminarTarifa, self).post(request, *args, **kwargs)

@method_decorator([login_required], name='dispatch')
class CrearEntradaVehiculo(CreateView):
    model = EntradaVehiculo
    template_name = 'parqueaderos/ingresar_vehiculo.html'
    form_class = EntradaVehiculoForm
    success_url = reverse_lazy('vehiculos-ingresados')
    context_object_name = 'tarifas_list'


    def get_context_data(self, **kwargs):
        context = super(CrearEntradaVehiculo, self).get_context_data(**kwargs)
        context['tarifas'] = Tarifa.objects.filter(anno=datetime.now().year)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            messages.success(request, 'Vehículo ingresado')
<<<<<<< HEAD
            return super(CrearEntradaVehiculo, self).post(request, kwargs)
=======
        return super(CrearEntradaVehiculo, self).post(request, *args, **kwargs)
>>>>>>> 4e877287c7578ecfb4d650280f8bc4430ba771e0


@method_decorator([login_required], name='dispatch')
class VerIngresados(ListView):
    model = EntradaVehiculo
    context_object_name = 'ingresados_list'
    template_name = 'parqueaderos/ingresados_list.html'