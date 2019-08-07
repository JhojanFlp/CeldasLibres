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

@method_decorator([login_required], name='dispatch')
class CrearClienteFrecuente(CreateView):
    template_name = 'parqueaderos/crear_clienteFrecuente.html'
    model = ClienteFrecuente
    form_class = CrearClienteFrecuenteForm
    success_url = reverse_lazy('parqueaderos')
    def post(self,request,*args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            tipo_documento=request.POST.get('parqueadero')
            identificacion=request.POST.get('identifiacion')
            nombres=request.POST.get('nombres')
            apellidos=request.POST.get('apellidos')
            num_cel=request.POST.get('celular')
            correo=request.POST.get('email')
            fecha_nac=request.POST.get('fecha_nacimiento')
            plan_pago=request.POST.get('planes_pago')
            messages.success(request, 'Cliente frecuente creado correctamente')
            client=ClienteFrecuente(identificacion=identificacion,tipo_documento=tipo_documento,
                nombres=nombres,apellidos=apellidos,numero_celular=num_cel,email=correo,
                fecha_nacimiento=fecha_nac,plan_pago=plan_pago)
            return render(request,self.template_name)
        else:
            messages.success(request, 'Error al crear cliente frecuente')
            return redirect('parqueaderos')

