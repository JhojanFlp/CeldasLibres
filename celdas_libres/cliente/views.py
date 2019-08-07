from django.shortcuts import render
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
from .models import ClienteFrecuente
from .forms import CrearClienteFrecuenteForm
from parqueaderos.models import PlanPago

@method_decorator([login_required], name='dispatch')
class CrearClienteFrecuente(CreateView):
    template_name = 'parqueaderos/crear_clienteFrecuente.html'
    model = ClienteFrecuente
    form_class = CrearClienteFrecuenteForm
    success_url = reverse_lazy('parqueaderos')

    def get_context_data(self, **kwargs):
    	context = super(CrearClienteFrecuente, self).get_context_data(**kwargs)
    	context['planes'] = PlanPago.objects.filter(eliminado='False')
    	return context

    def post(self,request,*args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            tipo_documento=request.POST.get('tipo_identificacion')
            identificacion=request.POST.get('identificacion')
            nombres=request.POST.get('nombres')
            apellidos=request.POST.get('apellidos')
            num_cel=request.POST.get('celular')
            correo=request.POST.get('email')
            fecha_nac=request.POST.get('fecha_nacimiento')
            plan_pag=request.POST.get('planes_pago')
            primary=PlanPago.objects.get(nombre=plan_pag, eliminado='False')
            client=ClienteFrecuente(identificacion=identificacion,tipo_documento=tipo_documento,
                nombres=nombres,apellidos=apellidos,numero_celular=num_cel,email=correo,
                fecha_nacimiento=fecha_nac,plan_pago=primary)
            client.save()
            messages.success(request, 'Cliente frecuente creado correctamente')
            return redirect('home')
        else:
            messages.warning(request, 'Error al crear cliente frecuente, Intente nuevamente')
            return redirect('crear-cliente-frecuente')
@method_decorator([login_required], name='dispatch')
class VerClientesFrecuentes(ListView):
    model = ClienteFrecuente
    context_object_name = 'cliente_frecuente'
    template_name = 'parqueaderos/clienteFrecuente_list.html'

