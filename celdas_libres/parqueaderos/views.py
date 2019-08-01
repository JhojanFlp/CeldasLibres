import datetime
import collections

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.db.models import Count

from vehiculos.models import Vehiculo

from .forms import (CrearCapacidadVehiculo, CrearParqueadero, CrearTarifaForm,
                    CreateDescuentoTarifa, CreatePlanPago, EntradaVehiculoForm, SalidaVehiculoForm,GenerarBalanceForm)
from .models import (CapacidadVehiculo, DescuentoTarifa, EntradaVehiculo,
                     Parqueadero, PlanPago, SalidaVehiculo, Tarifa, Factura)

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
        por_hora=request.POST.get('por_hora')
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

    #success_url = reverse_lazy('ficho-parqueadero')
    context_object_name = 'tarifas_list'

    def get_context_data(self, **kwargs):
        context = super(CrearEntradaVehiculo, self).get_context_data(**kwargs)
        context['tarifas'] = Tarifa.objects.filter(anno = datetime.date.today().year)
        context['parqueadero']=Parqueadero.objects.filter(encargado=self.request.user.id)
        context['user_id']=self.request.user.id
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            messages.success(request, 'Vehículo ingresado')
            return super(CrearEntradaVehiculo, self).post(request, kwargs)
        else:
            messages.warning(request, 'Debe tener asignado un parqueadero')
            return redirect('vehiculos-ingresados')

    def get_success_url(self):
        return reverse_lazy('ficho-parqueadero',args=(self.object.id,))

@method_decorator([login_required], name='dispatch')
class CrearSalidaVehiculo(CreateView):
    model = SalidaVehiculo
    template_name = 'parqueaderos/salida_vehiculo.html'
    form_class = SalidaVehiculoForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            messages.success(request, 'Salida registrada')
            salida = form.save(commit=False)
            salida.tipo_vehiculo = request.POST.get('tipo_vehiculo')
            salida.fecha_salida = request.POST.get('fecha_salida')
            salida.entrada_vehiculo = EntradaVehiculo.objects.get(
                pk=request.POST.get('entrada_vehiculo')
            )
            salida.operario = request.user.usuario
            salida.save()

            
            name = Parqueadero.objects.filter(encargado=request.user.usuario)[0].nombre
            phone = Parqueadero.objects.filter(nombre__contains=name)[0].telefono
            ubication = Parqueadero.objects.filter(nombre__contains=name)[0].direccion
            id_user = request.POST.get('documento')
            placa = request.POST.get('placa')                            
            in_date = datetime.datetime.strptime(request.POST.get('fecha_entrada'), '%d/%m/%Y %H:%M:%S')
            out_date = datetime.datetime.strptime(request.POST.get('fecha_salida'), '%d/%m/%Y %H:%M:%S')
            serial = 'gfK' + str(request.POST.get('fecha_salida'))
            request.session['serial']=serial
            print(Tarifa.objects.filter(tipo_vehiculo = request.POST.get('tipo_vehiculo'))[0].por_hora)
            total = ((out_date-in_date).seconds/3600) * Tarifa.objects.filter(tipo_vehiculo = request.POST.get('tipo_vehiculo'))[0].por_hora
            
            fact = Factura(serial=serial ,name= name, phone= phone, ubication= ubication, id_user= id_user, placa= placa, in_date= in_date, out_date=out_date, total = total)
            fact.save()

        else:
            messages.warning(request, 'Debe tener asignado un parqueadero')       

        return redirect('generar-factura')

    def get_context_data(self, **kwargs):
        context = super(CrearSalidaVehiculo, self).get_context_data(**kwargs)
        entrada = EntradaVehiculo.objects.get(pk=self.kwargs.get('pk'))
        context['entrada_vehiculo'] = entrada.id
        context['placa'] = entrada.placa
        context['tipo_vehiculo'] = entrada.tarifa.tipo_vehiculo
        context['fecha_entrada'] = entrada.fecha_ingreso.strftime('%d/%m/%Y %H:%M:%S')
        context['fecha_salida'] = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        return context

@method_decorator([login_required], name='dispatch')
class GenerarFactura(TemplateView):
    template_name = 'parqueaderos/generar_factura.html'
    #model = GenerarFactura
    

    """def get(self, request, *args, **kwargs):
        pk=request.session['serial']
        return redirect('generar-factura')"""

    def get_context_data(self, **kwargs):
        context = super(GenerarFactura, self).get_context_data(**kwargs)
        factura = Factura.objects.filter(serial = self.request.session['serial'])[0]
        context['name']= factura.name
        context['telefono']= factura.phone
        context['direccion']= factura.ubication
        context['id_usuario']= factura.id_user
        context['placa']= factura.placa
        context['entrada']= factura.in_date
        context['salida']= factura.out_date
        context['total']= factura.total
        return context
    
@method_decorator([login_required], name='dispatch')
class VerIngresados(ListView):
    model = EntradaVehiculo
    context_object_name = 'ingresados_list'
    template_name = 'parqueaderos/ingresados_list.html'

@method_decorator([login_required], name='dispatch')
class VerFicho(ListView):
    model = EntradaVehiculo
    context_object_name = 'ficho'
    template_name = 'parqueaderos/ficho.html'
    def get_context_data(self, **kwargs):
        context = super(VerFicho, self).get_context_data(**kwargs)
        context['ficho'] =EntradaVehiculo.objects.get(pk=self.kwargs.get('pk'))
        return context


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
    ordering = ['-creado']

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
    template_name = 'parqueaderos/crear_parqueadero.html'
    model = Parqueadero
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
        else:
            messages.error(request, 'Error al crear parqueadero')
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

@method_decorator([login_required, staff_member_required], name='dispatch')
class ModificarParqueadero(UpdateView):
    template_name = 'parqueaderos/parqueadero_update_form.html'
    model = Parqueadero
    form_class = CrearParqueadero
    success_url = reverse_lazy('parqueaderos')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        vehiculos = request.POST.getlist('vehiculo')
        capacidades = request.POST.getlist('capacidad')
        if form.is_valid():
            parqueadero = form.save()
            for vehiculo_id, capacidad in zip(vehiculos, capacidades):
                CapacidadVehiculo.objects.create(
                    parqueadero=parqueadero,
                    vehiculo=Vehiculo.objects.get(id=vehiculo_id),
                    capacidad=capacidad
                )
            messages.success(request, 'Parqueadero creado correctamente')
        return redirect(self.success_url)

@method_decorator([login_required, staff_member_required], name='dispatch')
class EliminarParqueadero(DeleteView):
    model = Parqueadero
    success_url = reverse_lazy('parqueaderos')

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Parqueadero eliminado correctamente')
        return super(EliminarParqueadero, self).post(request, *args, **kwargs)


@method_decorator([login_required], name='dispatch')
class VerBalance(ListView):
    model = EntradaVehiculo
    context_object_name = 'ingresados_list'
    template_name = 'parqueaderos/balance.html'
    def get_context_data(self, **kwargs):
        lista=[]
        lista2=[]
        dic={}
        dic2={}
        dic3={}
        total=0
        context = super(VerBalance, self).get_context_data(**kwargs)
        context['entradas'] = EntradaVehiculo.objects.values('tarifa__tipo_vehiculo').exclude(tarifa__tipo_vehiculo=None).annotate(num_ent=Count('tarifa__tipo_vehiculo'))
        nombres_entradas= EntradaVehiculo.objects.values('tarifa__tipo_vehiculo').distinct().exclude(tarifa__tipo_vehiculo=None).annotate(num_ent=Count('tarifa__tipo_vehiculo')).values_list('tarifa__tipo_vehiculo', flat='true')
        for nombres in nombres_entradas:
            lista.append(nombres)
        final=collections.Counter(lista)
        for clave, valor in final.items():
            dic[clave]=valor
            total=valor+total
        dic['Total']=total
        context['entradas_f']=dic
        
        salida= SalidaVehiculo.objects.all()
        for nombres in salida:
            lista2.append(nombres.tipo_vehiculo)
        final2=collections.Counter(lista2)
        for clave, valor in final2.items():
            dic2[clave]=valor
            dic3[clave]=valor
        tarifas = Tarifa.objects.all()
        total=0
        total2=0
        for tarifa in tarifas:
            if tarifa.tipo_vehiculo in dic2:
                clave=tarifa.tipo_vehiculo
                aux=int(dic2[clave])
                dic2[clave]=aux*tarifa.por_hora
                total=total+(aux*tarifa.por_hora)
                total2=total2+aux
        dic2['Total']=total
        dic3['Total']=total2
        context['balance']=dic2
        context['salidas']=dic3


        #context['salidas'] = SalidaVehiculo.objects.annotate(num_sal=Count('tipo_vehiculo'),nombre='tipo_vehiculo')
        #.values_list('tipo_vehiculo', flat='true')
        return context


@method_decorator([login_required, staff_member_required], name='dispatch')
class GenerarBalance(CreateView):
    template_name = 'parqueaderos/generar_balance.html'
    form_class = GenerarBalanceForm
    success_url =  reverse_lazy('home')
    def post(self, request, *args, **kwargs):
        messages.success(request, 'Parqueadero eliminado correctamente')
        return super(EliminarParqueadero, self).post(request, *args, **kwargs)

