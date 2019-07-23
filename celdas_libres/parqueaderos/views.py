import datetime

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from vehiculos.models import Vehiculo

from .forms import (CrearTarifaForm, CreateDescuentoTarifa, CreatePlanPago,
                    EntradaVehiculoForm, CrearParqueadero, CrearCapacidadVehiculo)
from .models import DescuentoTarifa, EntradaVehiculo, PlanPago, Tarifa, Parqueadero, CapacidadVehiculo

#import re






@method_decorator([login_required, staff_member_required], name='dispatch')
class CrearTarifa(CreateView):
    model = Tarifa
    template_name = 'parqueaderos/crear_tarifa.html'
    form_class = CrearTarifaForm
    success_url = reverse_lazy('tarifas')


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        anno = request.POST.get('anno')
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
        request.POST = request.POST.copy()
        request.POST['anno'] = datetime.date.today().year
        form = self.form_class(request.POST)
        #if form.is_valid():
        messages.success(request, 'Tarifa actualizada correctamente')
        return super(ModificarTarifa, self).post(request, *args, **kwargs)
        # else:
        #     messages.error(request, 'Tarifa no actualizada')
        #     return super(ModificarTarifa, self).post(request, *args, **kwargs)

@method_decorator([login_required, staff_member_required], name='dispatch')
class EliminarTarifa(DeleteView):
    model = Tarifa
    form_class = CrearTarifaForm
    success_url = reverse_lazy('tarifas')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

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
        context['tarifas'] = Tarifa.objects.filter(anno = datetime.date.today().year)#datetime.now().year)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            messages.success(request, 'Vehículo ingresado')
            return super(CrearEntradaVehiculo, self).post(request, kwargs)


@method_decorator([login_required], name='dispatch')
class VerIngresados(ListView):
    model = EntradaVehiculo
    context_object_name = 'ingresados_list'
    template_name = 'parqueaderos/ingresados_list.html'


@method_decorator([login_required, staff_member_required], name='dispatch')
class CrearPlanPago(CreateView):
    model = PlanPago
    template_name = 'parqueaderos/create_plan_pago.html'
    form_class = CreatePlanPago
    success_url = reverse_lazy('planes-pago')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        tarifas = request.POST.getlist('tarifa')
        descuentos = request.POST.getlist('descuento')
        if form.is_valid():
            plan_pago =  form.save()
            for tarifa_id, descuento in zip(tarifas, descuentos):
                DescuentoTarifa.objects.create(
                    plan_pago=plan_pago,
                    tarifa=Tarifa.objects.get(id=tarifa_id),
                    descuento=descuento
                )
            messages.success(request, 'Plan de pago creado correctamente')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super(CrearPlanPago, self).get_context_data(**kwargs)
        context['plan_form'] = self.form_class()
        context['descuento_form'] = CreateDescuentoTarifa()
        context['tarifas'] = Tarifa.objects.filter(anno=datetime.date.today().year)
        return context

@method_decorator([login_required], name='dispatch')
class VerPlanesPago(ListView):
    model = PlanPago
    context_object_name = 'planes_pago_list'
    template_name = 'parqueaderos/planes_pago.html'
    ordering  = ['-creado']

@method_decorator([login_required, staff_member_required], name='dispatch')
class ModificarPlanPago(UpdateView):
    model = PlanPago
    form_class = CreatePlanPago
    template_name = 'parqueaderos/plan_pago_update_form.html'
    success_url =  reverse_lazy('planes-pago')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        tarifas = request.POST.getlist('tarifa')
        descuentos = request.POST.getlist('descuento')
        if form.is_valid():
            plan_pago = PlanPago.objects.get(pk=kwargs['pk'])
            plan_pago.eliminado = True
            plan_pago.save()
            plan_pago = form.save()
            for tarifa_id, descuento in zip(tarifas, descuentos):
                DescuentoTarifa.objects.create(
                    plan_pago=plan_pago,
                    tarifa=Tarifa.objects.get(id=tarifa_id),
                    descuento=descuento
                )
            messages.success(request, 'Plan de pago modificado correctamente')
        return redirect(self.success_url)

@method_decorator([login_required, staff_member_required], name='dispatch')
class EliminarPlanPago(DeleteView):
    model = PlanPago
    success_url = reverse_lazy('planes-pago')

    def post(self, request, *args, **kwargs):
        plan_pago = PlanPago.objects.get(pk=kwargs['pk'])
        plan_pago.eliminado = True
        plan_pago.save()
        messages.success(request, 'Tarifa eliminada correctamente')
        return redirect(self.success_url)


@method_decorator([login_required, staff_member_required], name='dispatch')
class CrearParqueadero(CreateView):
    model = Parqueadero
    template_name = 'parqueaderos/crear_parqueadero.html'
    form_class = CrearParqueadero
    success_url = reverse_lazy('parqueaderos')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        vehiculos = request.POST.getlist('vehiculo')
        capacidades = request.POST.getlist('capacidad')
        if form.is_valid():
            parqueadero =  form.save()
            for vehiculo_id, capacidad in zip(vehiculos, capacidades):
                CapacidadVehiculo.objects.create(
                    parqueadero=parqueadero,
                    vehiculo=Vehiculo.objects.get(id=vehiculo_id),
                    capacidad=capacidad
                )
            messages.success(request, 'Parqueadero creado correctamente')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super(CrearParqueadero, self).get_context_data(**kwargs)
        context['parqueadero_form'] = self.form_class()
        context['capacidad_form'] = CrearCapacidadVehiculo()
        context['vehiculos'] =  Vehiculo.objects.all()
        return context

@method_decorator([login_required], name='dispatch')
class VerParqueaderos(ListView):
    model = Parqueadero
    context_object_name = 'parqueaderos_list'
    template_name = 'parqueaderos/parqueaderos.html'
