from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView,TemplateView, FormView
from Legajos.models import LegajosDerivaciones,HistorialLegajoIndices
from Legajos.forms import DerivacionesRechazoForm, LegajosDerivacionesForm
from django.db.models import Q
from .models import *
from Configuraciones.models import *
from .forms import *
from Usuarios.mixins import PermisosMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.db.models import Sum, F, ExpressionWrapper, IntegerField, Count, Max
import uuid
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from SIF_SL.models import *
from datetime import datetime, timedelta

# # Create your views here.
#derivaciones = LegajosDerivaciones.objects.filter(m2m_programas__nombr__iexact="MA")
#print(derivaciones)

class MADerivacionesBuscarListView(TemplateView, PermisosMixin):
    permission_required = "Usuarios.programa_MA"
    template_name = "SIF_MA/derivaciones_buscar.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        object_list = Legajos.objects.none()
        mostrar_resultados = False
        mostrar_btn_resetear = False
        query = self.request.GET.get("busqueda")

        if query:
            object_list = Legajos.objects.filter(Q(apellido__iexact=query) | Q(documento__iexact=query)).distinct()
            if object_list and object_list.count() == 1:
                id = None
                for o in object_list:
                    pk = Legajos.objects.filter(id = o.id).first()
                return redirect("legajosderivaciones_historial", pk.id)

            if not object_list:
                messages.warning(self.request, ("La búsqueda no arrojó resultados."))

            mostrar_btn_resetear = True
            mostrar_resultados = True

        context["mostrar_resultados"] = mostrar_resultados
        context["mostrar_btn_resetear"] = mostrar_btn_resetear
        context["object_list"] = object_list
        return self.render_to_response(context)


class MADerivacionesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_MA/derivaciones_bandeja_list.html"
    queryset = MA_Derivacion.objects.all()

    def get_context_data(self, **kwargs):
        context = super(MADerivacionesListView, self).get_context_data(**kwargs)

        model = MA_Derivacion.objects.all()

        context["todas"] = model
        context["pendientes"] = model.filter(estado="Pendiente")
        context["aceptadas"] = model.filter(estado="Aceptada")
        context["rechazadas"] = model.filter(estado="Rechazada")
        context["enviadas"] = model.filter(creado_por=self.request.user.id)
        return context

class MADerivacionesDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_MA/derivaciones_detail.html"
    model = LegajosDerivaciones

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(pk=pk, fk_programa=settings.PROG_MA).first()
        archivos = LegajosDerivacionesArchivos.objects.filter(legajo_derivacion=pk).all()
        context["pk"] = pk
        context["archivos"] = archivos
        return context

class MADerivacionesRechazo(PermisosMixin, CreateView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_MA/derivaciones_rechazo.html"
    form_class = DerivacionesRechazoForm

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(pk=pk, fk_programa=settings.PROG_MA).first()
        context["object"] = legajo
        return context
    
    def form_valid(self, form):
        pk = self.kwargs["pk"]
        base = LegajosDerivaciones.objects.get(pk=pk)
        base.motivo_rechazo = form.cleaned_data['motivo_rechazo']
        base.obs_rechazo = form.cleaned_data['obs_rechazo']
        base.estado = "Rechazada"
        base.fecha_rechazo = date.today()
        base.save() 
        return HttpResponseRedirect(reverse('MA_derivaciones_listar'))
    
    def form_invalid(self, form):
        return super().form_invalid(form)   
    
    def get_success_url(self):
        return reverse('MA_derivaciones_listar')
    
class MADerivacionesUpdateView(PermisosMixin, UpdateView):
    permission_required = "Usuarios.rol_admin"
    model = LegajosDerivaciones
    template_name = "SIF_MA/derivaciones_form.html"
    form_class = LegajosDerivacionesForm
    success_message = "Derivación editada con éxito"

    def get_initial(self):
        initial = super().get_initial()
        initial["fk_usuario"] = self.request.user
        return initial
        
    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(id=pk).first()
        context["legajo"] = Legajos.objects.filter(id=legajo.fk_legajo.id).first()
        return context
    
    def form_invalid(self, form):
        return super().form_invalid(form)   
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('MA_derivaciones_ver', kwargs={'pk': pk})

class MAPreAdmisionesCreateView(PermisosMixin, CreateView, SuccessMessageMixin):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_MA/preadmisiones_form.html"
    form_class = MA_MultiModelForm
    success_message = "Preadmisión creada correctamente"

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        legajo = MA_Derivacion.objects.filter(pk=pk).first()
        responsables = LegajoGrupoFamiliar.objects.filter(fk_legajo_1=legajo.fk_expediente.fk_derivacion.fk_legajo.id, vinculo="Referente")
        responsables2 = LegajoGrupoFamiliar.objects.filter(fk_legajo_2=legajo.fk_expediente.fk_derivacion.fk_legajo.id, vinculo_inverso="Referente")
        context["pk"] = pk
        context["legajo"] = legajo
        context["responsables"] = responsables
        context["responsables2"] = responsables2
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop('instance', None)  # Eliminamos el argumento 'instance' si está presente
        return kwargs

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        fecha_actual = datetime.now()
        i45 = fecha_actual + timedelta(days=45)
        i90 = fecha_actual + timedelta(days=90)
        i135 = fecha_actual + timedelta(days=135)
        i180 = fecha_actual + timedelta(days=180)

        preadmision_data = {
            'fk_derivacion_id': pk,
            'fk_legajo': form.cleaned_data['fk_legajo'],
            'PER': form.cleaned_data['PER'],
            'juzgado': form.cleaned_data['juzgado'],
            'REUNA': form.cleaned_data['REUNA'],
            'organismo_municipal': form.cleaned_data['organismo_municipal'],
            'organismo_zonal': form.cleaned_data['organismo_zonal'],
            'estado': "En proceso",
            'creado_por_id' : self.request.user.id,
            'i45' : i45,
            'i90' : i90,
            'i135' : i135,
            'i180' : i180,
        }
        preadmi_instance = MA_PreAdmision.objects.create(**preadmision_data)

        familia_abrigadora = self.request.POST.getlist('familia_abrigadora'),
        if familia_abrigadora:
            for familiar in familia_abrigadora:
                for f in familiar:
                    familia = MA_Familia_Abrigadora(fk_preadmi=preadmi_instance, fk_legajo_id=f)
                    familia.save()

        archivos = self.request.FILES.getlist('archivos')
        for archivo in archivos:
            preadmi_archivo = MA_Preadmision_Archivos(fk_preadmi=preadmi_instance, archivo=archivo)
            preadmi_archivo.save()

        base = MA_Derivacion.objects.get(pk=pk)
        base.estado = "Aceptada"
        base.save() 
        
        return redirect('MA_expediente_ver', pk=base.pk)


class MAPreAdmisionesUpdateView(PermisosMixin, UpdateView, SuccessMessageMixin):
    permission_required = "Usuarios.rol_admin"
    model = MA_PreAdmision
    form_class = MA_MultiModelForm 
    template_name = 'SIF_MA/preadmisiones_form.html'
    success_message = "Preadmisión actualizada correctamente"

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        legajo = MA_PreAdmision.objects.filter(pk=pk).first()
        context["pk"] = pk
        context["legajo"] = legajo
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop('instance', None) 
        return kwargs

    def form_valid(self, form):
        pk = self.kwargs["pk"]

        preadmi_instance = form.save(commit=False)
        preadmi_instance.estado = "En proceso"
        preadmi_instance.creado_por_id = self.request.user.id
        preadmi_instance.save()

        familia_abrigadora = self.request.POST.getlist('familia_abrigadora'),
        if familia_abrigadora:
            for familiar in familia_abrigadora:
                for f in familiar:
                    familia = MA_Familia_Abrigadora(fk_preadmi=preadmi_instance, fk_legajo_id=f)
                    familia.save()

        archivos = self.request.FILES.getlist('archivos')
        for archivo in archivos:
            preadmi_archivo = MA_Preadmision_Archivos(fk_preadmi=preadmi_instance, archivo=archivo)
            preadmi_archivo.save()
        
        return redirect('MA_preadmisiones_ver', pk=preadmi_instance.pk)


class MAPreAdmisionesDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_MA/preadmisiones_detail.html"
    model = MA_PreAdmision

    def get_context_data(self, **kwargs):
        pk = MA_PreAdmision.objects.filter(pk=self.kwargs["pk"]).first()
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(pk=pk.fk_derivacion_id).first()
        archivos = MA_Preadmision_Archivos.objects.filter(fk_preadmi_id = pk)
        context["archivos"] = archivos
        context["legajo"] = legajo
        return context
    
    def post(self, request, *args, **kwargs):
        if 'finalizar_preadm' in request.POST:
            # Realiza la actualización del campo aquí
            objeto = self.get_object()
            objeto.save()

            admi = MA_Admision(fk_preadmi=objeto)
            admi.save()
        
            return redirect('MA_admisiones_crear', pk=admi.pk)

class MAPreAdmisionesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_MA/preadmisiones_list.html"
    model = MA_PreAdmision

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pre_admi = MA_PreAdmision.objects.all()
        context["object"] = pre_admi
        return context

class MAPreAdmisionesBuscarListView(PermisosMixin, TemplateView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_MA/preadmisiones_buscar.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        object_list = MA_PreAdmision.objects.none()
        mostrar_resultados = False
        mostrar_btn_resetear = False
        query = self.request.GET.get("busqueda")
        if query:
            object_list = MA_PreAdmision.objects.filter(Q(fk_legajo__apellido__iexact=query) | Q(fk_legajo__documento__iexact=query), fk_derivacion__fk_programa_id=25).exclude(estado__in=['Rechazada','Aceptada']).distinct()
            #object_list = Legajos.objects.filter(Q(apellido__iexact=query) | Q(documento__iexact=query))
            if not object_list:
                messages.warning(self.request, ("La búsqueda no arrojó resultados."))

            mostrar_btn_resetear = True
            mostrar_resultados = True

        context["mostrar_resultados"] = mostrar_resultados
        context["mostrar_btn_resetear"] = mostrar_btn_resetear
        context["object_list"] = object_list

        return self.render_to_response(context)

class MAPreAdmisionesDeleteView(PermisosMixin, DeleteView):
    permission_required = "Usuarios.rol_admin"
    model = MA_PreAdmision
    template_name = "SIF_MA/preadmisiones_confirm_delete.html"
    success_url = reverse_lazy("MA_preadmisiones_listar")

    def form_valid(self, form):
        if self.object.estado != "En proceso":
            messages.error(
                self.request,
                "No es posible eliminar una solicitud en estado " + self.object.estado,
            )

            return redirect("MA_preadmisiones_ver", pk=int(self.object.id))

        if self.request.user.id != self.object.creado_por.id:
            messages.error(
                self.request,
                "Solo el usuario que generó esta derivación puede eliminarla.",
            )

            return redirect("MA_preadmisiones_ver", pk=int(self.object.id))

        else:
            self.object.delete()
            return redirect(self.success_url)


class MAAdmisionesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_MA/adminsiones_list.html"
    model = MA_Admision

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        admi = MA_Admision.objects.all()

        context["admi"] = admi
        return context
    
class MAAdmisionesCreateView(PermisosMixin, CreateView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_MA/admisiones_form.html"
    form_class = MA_AdmisionForm
    model = MA_Admision
    
    def get_context_data(self, **kwargs):
        pk = self.kwargs.get("pk")
        admi = MA_Admision.objects.filter(pk=pk).first()
        preadmi_ma = MA_PreAdmision.objects.filter(pk=pk).first()
        context = super().get_context_data(**kwargs)

        context["preadmi_ma"] = preadmi_ma
        return context
    
    def post(self, request, *args, **kwargs):        
        if 'confirmar_admi' in request.POST:
            pk = self.kwargs.get("pk")
            objeto = MA_Admision()
            fecha_ingreso = request.POST.get('fecha_ingreso')
            tipo_abrigo = request.POST.get('tipo_abrigo')
            equipo_trabajo = request.POST.get('equipo_trabajo')
            organismo = request.POST.get('organismo')
            objeto.fecha_ingreso = fecha_ingreso
            objeto.tipo_abrigo = tipo_abrigo
            objeto.equipo_trabajo = equipo_trabajo
            objeto.organismo = organismo
            objeto.fk_preadmi_id = pk
            objeto.creado_por_id = self.request.user.id
            objeto.save()
            preadmi = MA_PreAdmision.objects.get(pk=pk)
            preadmi.estado = 'Activa'
            preadmi.save()
            return redirect('MA_expediente_ver', pk=preadmi.fk_derivacion.id)
    
    
    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

class MAAdmisionesUpdateView(PermisosMixin, UpdateView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_MA/admisiones_form.html"
    form_class = MA_AdmisionForm

class MAAdmisionesDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.rol_admin"
    model = MA_Admision
    template_name = 'SIF_MA/admisiones_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = MA_Admision.objects.filter(pk=self.kwargs["pk"]).first()
        admi = MA_Admision.objects.filter(pk=self.kwargs["pk"]).first()
        preadmi = MA_PreAdmision.objects.filter(pk=pk.fk_preadmi_id).first()
        intervenciones = MA_Intervenciones.objects.filter(fk_admision_id=admi.id).all()
        context["intervenciones"] = intervenciones
        return context


class MAAsignadoAdmisionDetail(PermisosMixin, DetailView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_MA/asignado_admisiones_detail.html"
    model = MA_Admision

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        admi = MA_Admision.objects.filter(pk=self.kwargs["pk"]).first()

        preadmi = MA_PreAdmision.objects.filter(pk=admi.fk_preadmi_id).first()
        intervenciones = MA_Intervenciones.objects.filter(fk_admision_id=admi.id).all()
        intervenciones_last = MA_Intervenciones.objects.filter(fk_admision_id=admi.id).last()

        context["object"] = admi
        context["vo"] = self.object
        context["intervenciones_count"] = intervenciones.count()
        context["intervenciones_last"] = intervenciones_last
        
        return context

class MAInactivaAdmisionDetail(PermisosMixin, DetailView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_MA/inactiva_admisiones_detail.html"
    model = MA_Admision

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        admi = MA_Admision.objects.filter(pk=self.kwargs["pk"]).first()

        preadmi = MA_PreAdmision.objects.filter(pk=admi.fk_preadmi_id).first()
        intervenciones = MA_Intervenciones.objects.filter(fk_admision_id=admi.id).all()
        intervenciones_last = MA_Intervenciones.objects.filter(fk_admision_id=admi.id).last()

        context["object"] = admi
        context["vo"] = self.object
        context["intervenciones_count"] = intervenciones.count()
        context["intervenciones_last"] = intervenciones_last
        
        return context



class MAIntervencionesCreateView(PermisosMixin, CreateView):
    permission_required = "Usuarios.rol_admin"
    model = MA_Intervenciones  # Debería ser el modelo MA_Intervenciones
    template_name = "SIF_MA/intervenciones_form.html"
    form_class = MA_IntervencionesForm

    def form_valid(self, form):
        form.instance.fk_admision_id = self.kwargs["pk"]
        form.instance.creado_por_id = self.request.user.id
        self.object = form.save()

        return redirect('MA_admisiones_ver', pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = MA_Admision.objects.get(pk=self.kwargs["pk"])  # Obtén el objeto directamente
        context["form"] = self.get_form()  # Obtiene una instancia del formulario

        return context
    
class MAIntervencionesUpdateView(PermisosMixin, UpdateView):
    permission_required = "Usuarios.rol_admin"
    model = MA_Intervenciones
    template_name = "SIF_MA/intervenciones_form.html"
    form_class = MA_IntervencionesForm

    def form_valid(self, form):
            pk = MA_Intervenciones.objects.filter(pk=self.kwargs["pk"]).first()
            admi = MA_Admision.objects.filter(id=pk.fk_admision.id).first()
            form.instance.fk_admision_id = admi.id
            form.instance.modificado_por_id = self.request.user.id
            self.object = form.save()
        
            return redirect('MA_intervencion_ver', self.object.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = MA_Intervenciones.objects.filter(pk=self.kwargs["pk"]).first()
        admi = MA_Admision.objects.filter(id=pk.fk_admision.id).first()

        context["object"] = admi

        return context

class MAIntervencionesLegajosListView(PermisosMixin, DetailView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_MA/intervenciones_legajo_list.html"
    model = MA_Admision

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        admi = MA_Admision.objects.filter(pk=self.kwargs["pk"]).first()
        intervenciones = MA_Intervenciones.objects.filter(fk_admision_id=admi.id).all()
        intervenciones_last = MA_Intervenciones.objects.filter(fk_admision_id=admi.id).last()
        preadmi = MA_PreAdmision.objects.filter(pk=admi.fk_preadmi_id).first()

        context["object"] = admi
        context["intervenciones"] = intervenciones
        context["intervenciones_count"] = intervenciones.count()
        context["intervenciones_last"] = intervenciones_last

        return context
    
class MAIntervencionesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_MA/intervenciones_list.html"
    model = MA_Intervenciones

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        intervenciones = MA_Intervenciones.objects.all()
        context["intervenciones"] = intervenciones
        return context

class MAIntervencionesDetail (PermisosMixin, DetailView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_MA/intervencion_detail.html"
    model = MA_Intervenciones

class MAIntervencionesDeleteView(PermisosMixin, DeleteView):
    permission_required = "Usuarios.rol_admin"
    model = MA_Intervenciones
    template_name = "SIF_MA/intervenciones_confirm_delete.html"
    success_url = reverse_lazy("MA_intervenciones_listar")

    def form_valid(self, form):

        if self.request.user.id != self.object.creado_por.id:
            print(self.request.user)
            print(self.object.creado_por)
            messages.error(
                self.request,
                "Solo el usuario que generó esta derivación puede eliminarla.",
            )

            return redirect("MA_preadmisiones_ver", pk=int(self.object.id))

        else:
            self.object.delete()
            return redirect(self.success_url)
        

class MAAdmisionesBuscarListView(PermisosMixin, TemplateView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_MA/admisiones_buscar.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        object_list = MA_PreAdmision.objects.none()
        mostrar_resultados = False
        mostrar_btn_resetear = False
        query = self.request.GET.get("busqueda")
        if query:
            object_list = MA_Admision.objects.filter(Q(fk_preadmi__fk_legajo__apellido__iexact=query) | Q(fk_preadmi__fk_legajo__documento__iexact=query), fk_preadmi__fk_derivacion__fk_programa_id=25).exclude(estado__in=['Rechazada','Aceptada']).distinct()
            if not object_list:
                messages.warning(self.request, ("La búsqueda no arrojó resultados."))

            mostrar_btn_resetear = True
            mostrar_resultados = True

        context["mostrar_resultados"] = mostrar_resultados
        context["mostrar_btn_resetear"] = mostrar_btn_resetear
        context["object_list"] = object_list

        return self.render_to_response(context)
    

class MA_ExpedienteDetailView(PermisosMixin, DetailView):
    permission_required = ['Usuarios.rol_admin','Usuarios.rol_observador','Usuarios.rol_consultante']
    template_name = "SIF_MA/expediente_detail.html"
    model = MA_Derivacion
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs["pk"]
        derivacion = MA_Derivacion.objects.filter(pk=id).first()
        preadmi_ma = MA_PreAdmision.objects.filter(fk_derivacion_id=derivacion.pk).first()
        if preadmi_ma:
            documentacion = MA_Preadmision_Archivos.objects.filter(fk_preadmi_id=preadmi_ma.pk).all()
            documentacion_adicional = MA_Expedientes_Archivos.objects.filter(fk_derivacion_id=id).all()
            admi = MA_Admision.objects.filter(fk_preadmi_id=preadmi_ma.id).first()
            familia_abrigadora = MA_Familia_Abrigadora.objects.filter(fk_preadmi_id=preadmi_ma.pk).all()
        else:
            documentacion = []
            documentacion_adicional = []
            admi = []
            familia_abrigadora = []
        pk = SL_Expedientes.objects.filter(pk=derivacion.fk_expediente_id).first()
        preadmi = SL_PreAdmision.objects.filter(fk_expediente_id=pk).last()
        familia = SL_GrupoFamiliar.objects.filter(fk_expediente_id=pk).all()
        legajos_alertas = LegajoAlertas.objects.filter(fk_legajo=preadmi.fk_derivacion.fk_legajo)
        archivos = SL_ExpedientesArchivos.objects.filter(fk_expediente_id=pk).all()
        archivos_derivacion = LegajosDerivacionesArchivos.objects.filter(legajo_derivacion_id=preadmi.fk_derivacion_id).all()
        resultado = SL_IndiceVulnerabilidad.objects.filter(fk_expediente_id=preadmi.fk_expediente_id)
        equipo = SL_EquipoDesignado.objects.filter(fk_expediente_id=preadmi.fk_expediente_id).first()
        referentes = SL_Referentes.objects.filter(fk_expediente_id=preadmi.fk_expediente_id).all()
        intervenciones = SL_Intervenciones.objects.filter(fk_expediente_id=preadmi.fk_expediente_id).all()
        

        context['admi'] = admi
        context['preadmi'] = preadmi
        context['documentacion'] = documentacion
        context['documentacion_adicional'] = documentacion_adicional
        context['preadmi_ma'] = preadmi_ma
        context['legajos_alertas'] = legajos_alertas
        context['familia'] = familia
        context['archivos'] = archivos
        context['archivos_derivacion'] = archivos_derivacion
        context['equipo'] = equipo
        context['referentes'] = referentes
        context['intervenciones'] = intervenciones
        context['familia_abrigadora'] = familia_abrigadora
        context['resultado'] = resultado.aggregate(total=Sum('fk_indice__puntaje'))
        context['hoy'] = datetime.now().date()
        return context
    
    def post(self, request, *args, **kwargs):
        pk=self.kwargs["pk"]
        if '45' in self.request.FILES:
            archivo45 = request.FILES.get('45')
            instancia = MA_PreAdmision.objects.filter(fk_derivacion_id=pk).first()
            if instancia:
                instancia.archivo45 = archivo45
                instancia.save()
            
        if '90' in self.request.FILES:
            archivo90 = request.FILES.get('90')
            instancia = MA_PreAdmision.objects.filter(fk_derivacion_id=pk).first()
            if instancia:
                instancia.archivo90 = archivo90
                instancia.save()

        if '135' in self.request.FILES:
            archivo135 = request.FILES.get('135')
            instancia = MA_PreAdmision.objects.filter(fk_derivacion_id=pk).first()
            if instancia:
                instancia.archivo135 = archivo135
                instancia.save()
        
        if 'archivos' in self.request.FILES:
            archivos = self.request.FILES.getlist('archivos')
            for archivo in archivos:
                MA_Expedientes_Archivos.objects.create(fk_derivacion_id=pk, archivo=archivo)

        return redirect('MA_expediente_ver', pk)

class MA_ExpedienteListView(PermisosMixin, ListView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_MA/expediente_list.html"
    model = MA_Admision

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hoy'] = datetime.now().date()
        return context