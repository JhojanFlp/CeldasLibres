import datetime
import pytz

local_tz = pytz.timezone('America/Bogota')

import collections
from django.utils import timezone
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView , FormView , View
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.db.models import Count
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse,HttpResponseRedirect
from django.template import context
from django.forms import formset_factory
from django.http import JsonResponse

from vehiculos.models import Vehiculo

from .forms import (CrearCapacidadVehiculo, CrearParqueaderoForm, CrearTarifaForm,
                    CreateDescuentoTarifa, CreatePlanPago, EntradaVehiculoForm, SalidaVehiculoForm,GenerarBalanceForm)
from .models import (CapacidadVehiculo, DescuentoTarifa, EntradaVehiculo,
                     Parqueadero, PlanPago, SalidaVehiculo, Tarifa, Factura)

from cliente.models import ClienteFrecuente

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

    def get_context_data(self,**kwargs):
        context = super(CrearEntradaVehiculo, self).get_context_data(**kwargs)
        parqueaderosxencargado = Parqueadero.objects.filter(encargado=self.request.user.usuario).count()
        print(parqueaderosxencargado)
        if(parqueaderosxencargado==0):
            #context['messages']= ('Debe tener asignado un parqueadero')
            messages.warning(self.request, 'Debe tener asignado un parqueadero')
            messages.warning(self.request, 'Los campos se desbloquearan cuando tenga asignado un parqueadero')
            context['identificacion']=0
            template_name = 'parqueaderos/vehiculos-ingresados.html'
            print('entre al if')
        else:
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

def utc_to_local(utc_dt):
    local_dt= utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)

@method_decorator([login_required], name='dispatch')
class CrearSalidaVehiculo(CreateView):
    model = SalidaVehiculo
    template_name = 'parqueaderos/salida_vehiculo.html'
    form_class = SalidaVehiculoForm

    def post(self, request, *args, **kwargs):
        parqueaderosxencargado = Parqueadero.objects.filter(encargado=request.user.usuario).count()
        if(parqueaderosxencargado==0):
            messages.warning(request, 'Debe tener asignado un parqueadero')
            return redirect('vehiculos-ingresados')

        entrada_pk = request.POST.get('entrada_vehiculo')
        entradaVehiculo = EntradaVehiculo.objects.get(pk=entrada_pk)
        if(entradaVehiculo.estado_facturado==True):
            messages.warning(request, 'La salida del vehiculo ya ha sido facturada')
            return redirect('historial-salidas')
        
        form = self.form_class(request.POST)
        if form.is_valid():
            messages.success(request, 'Salida registrada y factura generada')
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
            tipo_vehiculo  = request.POST.get('tipo_vehiculo')
            in_date = datetime.datetime.strptime(request.POST.get('fecha_entrada'), '%d/%m/%Y %H:%M:%S')
            out_date = datetime.datetime.strptime(request.POST.get('fecha_salida'), '%d/%m/%Y %H:%M:%S')
            serial = 'gfK' + str(request.POST.get('fecha_salida'))
            nameOP = self.request.user.username
            request.session['serial']=serial
            print(Tarifa.objects.filter(tipo_vehiculo = request.POST.get('tipo_vehiculo'))[0].por_hora)
            total_general = ((out_date-in_date).seconds/3600) * Tarifa.objects.filter(tipo_vehiculo = request.POST.get('tipo_vehiculo'))[0].por_hora
            print("Total antes de descuentos ", total_general)

            if id_user:
                try:
                    cliente = ClienteFrecuente.objects.get(identificacion=id_user)
                    plan_pago=cliente.plan_pago
                    descuento=plan_pago.descuentos.all().filter(tarifa__tipo_vehiculo=tipo_vehiculo)[0]
                    total=total_general*(1-(float(descuento.descuento/100)))
                    print("Se selecciono: ", descuento.tarifa, ", Descuento:", descuento.descuento, ", Total a Facturar: ", total)
                    descuento=float(descuento.descuento)
                except:
                    plan_pago= None
                    descuento= 0
                    total=total_general
                    print("no es cliente con plan de pago")

            entradaVehiculo.estado_facturado = True
            entradaVehiculo.save()


            fact = Factura(serial=serial ,name= name, nameOP=nameOP, phone= phone, ubication= ubication, id_user= id_user, placa= placa, tipo_vehiculo=tipo_vehiculo, in_date= in_date, out_date=out_date, total_general=total_general, descuento=descuento, total = total)
            fact.save()

        else:
            messages.warning(request, 'Debe tener asignado un parqueadero')       
 
        return redirect('generar-factura')

    def get_context_data(self, **kwargs):
        context = super(CrearSalidaVehiculo, self).get_context_data(**kwargs)
        entrada = EntradaVehiculo.objects.get(pk=self.kwargs.get('pk'))
        context['documento'] = entrada.identificacion
        context['entrada_vehiculo'] = entrada.id
        context['placa'] = entrada.placa
        context['tipo_vehiculo'] = entrada.tarifa.tipo_vehiculo
        context['fecha_entrada'] = utc_to_local(entrada.fecha_ingreso).strftime('%d/%m/%Y %H:%M:%S')
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
        context['tipo_vehiculo']= factura.tipo_vehiculo
        context['total']= factura.total
        context['total_general']= factura.total_general
        context['descuento']= factura.descuento
        return context


@method_decorator([login_required], name='dispatch')
class VerIngresados(ListView):
    model = EntradaVehiculo
    context_object_name = 'ingresados_list'
    template_name = 'parqueaderos/ingresados_list.html'
    def get_context_data(self,**kwargs):
    #    print("estoy al principio")
        context = super(VerIngresados, self).get_context_data(**kwargs)
    #    print("estoy antes del filtro")
        parqueaderosxencargado = Parqueadero.objects.filter(encargado=self.request.user.usuario).count()
    #    print("estoy despues del filtro")
    #    print(parqueaderosxencargado)
        if(parqueaderosxencargado==0):
    #        #context['messages']= ('Debe tener asignado un parqueadero')
            messages.warning(self.request, 'Debe tener asignado un parqueadero para registrar vehiculos')
            context['parqueadero']=0
            print('entre al if')
        else:
            context['parqueadero']=parqueaderosxencargado
    #        print('no entre al if')
        return context

    def get_queryset(self):
        try:
            query = super(VerIngresados, self).get_queryset()
            parking = Parqueadero.objects.filter(encargado=self.request.user.usuario)[0]
            return query.filter(parqueadero=parking)
        except:
            messages.warning(self.request, 'Debe tener asignado un parqueadero para registrar vehiculos')
        #    context['parqueadero']=0


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
    form_class = CrearParqueaderoForm
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
    form_class = CrearParqueaderoForm
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
        parq=self.kwargs.get('parqueadero')
        desde=self.kwargs.get('desde')
        desdetime=datetime.datetime.strptime(desde, '%Y-%m-%d')
        hasta=self.kwargs.get('hasta')
        hastatime=datetime.datetime.strptime(hasta, '%Y-%m-%d')
        lista=[]
        lista2=[]
        dic={}
        dic2={}
        dic3={}
        new={}
        total=0
        #fecha_ingreso=[desdetime, hastatime]
        context = super(VerBalance, self).get_context_data(**kwargs)
        nombres_entradas= EntradaVehiculo.objects.values('tarifa__tipo_vehiculo').filter(parqueadero__nombre=parq).exclude(tarifa__tipo_vehiculo=None).annotate(num_ent=Count('tarifa__tipo_vehiculo')).values_list('tarifa__tipo_vehiculo', flat='true')
        for nombres in nombres_entradas:
            lista.append(nombres)
        final=collections.Counter(lista)
        for clave, valor in final.items():
            dic[clave]=valor
            total=valor+total
        #dic=sorted(dic.items())
        dic['Total']=total
        context['entradas_f']=dic
        
        salida= SalidaVehiculo.objects.filter(operario__parqueadero__nombre=parq)
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
        primer=EntradaVehiculo.objects.first()
        context['fecha_entrada']=desde
        first=primer.fecha_ingreso
        context['fecha_salida']=hasta
        diff=hastatime-desdetime
        context['fecha_total']=diff.days
        context['parq']=parq
        return context

@method_decorator([login_required, staff_member_required], name='dispatch')
class GenerarBalance(FormView):
    template_name = 'parqueaderos/generar_balance.html'
    form_class = GenerarBalanceForm
    success_url =  reverse_lazy('ver-balance')
    #def get(self,request):
     #   form = self.form_class()

    def post(self,request,*args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            parq=request.POST.get('parqueadero')
            since=request.POST.get('desde')
            until=request.POST.get('hasta')
            messages.success(request, 'Busqueda correcta')
            args={'parqueadero':parq,'desde':since,'hasta':until}
            return redirect('ver-balance',parqueadero=parq,desde=since,hasta=until)
        else:
            messages.success(request, 'No dio')
            return render(request,self.template_name)

@method_decorator([login_required], name='dispatch')
class HistorialSalidas(ListView):
    model = Factura
    context_object_name = 'facturas_list'
    template_name = 'parqueaderos/historial-salidas.html'


@method_decorator([login_required], name='dispatch')
class HistorialFacturas(ListView):
    model = Factura
    context_object_name = 'facturas_list'
    template_name = 'parqueaderos/historial-facturas.html'

def buscar_cliente(request, identificacion):
    if request.is_ajax():
        try:
            cliente = ClienteFrecuente.objects.get(identificacion=identificacion)
            return JsonResponse({
                'name': cliente.nombres,
                'lastname': cliente.apellidos
            })
        except:
            return JsonResponse({
                'name': None,
                'lastname': None
            })


