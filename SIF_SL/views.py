from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView,TemplateView, FormView, View
from Legajos.models import *
from Legajos.forms import DerivacionesRechazoForm, LegajosDerivacionesForm
from django.db.models import Q
from .models import *
from Configuraciones.models import *
from .forms import *
from Usuarios.mixins import PermisosMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Sum, F, ExpressionWrapper, IntegerField, Count, Max
import uuid
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings


# # Create your views here.

class SLDerivacionesBuscarListView(TemplateView, PermisosMixin):
    permission_required = "Usuarios.programa_SL"
    template_name = "SIF_SL/derivaciones_buscar.html"

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


class SLDerivacionesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_SL/derivaciones_bandeja_list.html"
    queryset = LegajosDerivaciones.objects.filter(fk_programa=settings.PROG_SL)

    def get_context_data(self, **kwargs):
        context = super(SLDerivacionesListView, self).get_context_data(**kwargs)

        model = self.queryset

        query = self.request.GET.get("busqueda")

        if query:
            object_list = LegajosDerivaciones.objects.filter((Q(fk_legajo__apellido__iexact=query) | Q(fk_legajo__nombre__iexact=query)) & Q(fk_programa=settings.PROG_SL)).distinct()
            context["object_list"] = object_list
            model = object_list
            if not object_list:
                messages.warning(self.request, ("La búsqueda no arrojó resultados."))

        context["todas"] = model
        context["pendientes"] = model.filter(estado="Pendiente")
        context["aceptadas"] = model.filter(estado="Aceptada")
        context["rechazadas"] = model.filter(estado="Rechazada")
        context["enviadas"] = model.filter(fk_usuario=self.request.user)
        return context

class SLDerivacionesDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_SL/derivaciones_detail.html"
    model = LegajosDerivaciones

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(pk=pk, fk_programa=settings.PROG_SL).first()
        context["pk"] = pk
        return context

class SLDerivacionesRechazo(PermisosMixin, CreateView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_SL/derivaciones_rechazo.html"
    form_class = DerivacionesRechazoForm

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(pk=pk, fk_programa=settings.PROG_SL).first()
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
        return HttpResponseRedirect(reverse('SL_derivaciones_listar'))
    
    def form_invalid(self, form):
        return super().form_invalid(form)   
    
    def get_success_url(self):
        return reverse('SL_derivaciones_listar')
    
class SLDerivacionesUpdateView(PermisosMixin, UpdateView):
    permission_required = "Usuarios.rol_admin"
    model = LegajosDerivaciones
    template_name = "SIF_SL/derivaciones_form.html"
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
        return reverse('SL_derivaciones_ver', kwargs={'pk': pk})


class SLPreAdmisionesCreateView(PermisosMixin,FormView, SuccessMessageMixin):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_SL/preadmisiones_form.html"
    form_class = SL_MultiModelForm
    success_message = "Preadmisión creada correctamente"

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(pk=pk).first()
        familiares_fk1 = LegajoGrupoFamiliar.objects.filter(fk_legajo_1=legajo.fk_legajo.id, vinculo="Hermano/a").all()
        familiares_fk2 = LegajoGrupoFamiliar.objects.filter(fk_legajo_2=legajo.fk_legajo.id, vinculo_inverso="Hermano/a").all()
        categorias_alertas = CategoriaAlertas.objects.all()
        alertas = Alertas.objects.all()
        responsables = LegajoGrupoFamiliar.objects.filter(fk_legajo_1=legajo.fk_legajo.id).exclude(vinculo="Hermano/a")
        responsables2 = LegajoGrupoFamiliar.objects.filter(fk_legajo_2=legajo.fk_legajo.id).exclude(vinculo_inverso="Hermano/a")
        
        context["pk"] = pk
        context["legajo"] = legajo
        context["categorias_alertas"] = categorias_alertas
        context["alertas"] = alertas
        context["count_familia"] = familiares_fk1.count() + familiares_fk2.count()
        context["familiares_fk1"] = familiares_fk1
        context["familiares_fk2"] = familiares_fk2
        context["count_referentes"] = responsables.count() + responsables2.count()
        context["responsables"] = responsables
        context["responsables2"] = responsables2
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['pk_url'] = self.kwargs["pk"]  # Pasar el pk de la URL al formulario
        return kwargs
    
    def form_valid(self, form):
        pk = self.kwargs["pk"]
        expediente_data = {
            'expediente': form.cleaned_data['expediente'],
            'fk_derivacion': form.cleaned_data['fk_derivacion'],
            'fk_equipo': form.cleaned_data['fk_equipo'],
            'creado_por_id': self.request.user.id,
            'modificado_por': form.cleaned_data['modificado_por'],
            'estado': "Iniciado",
        }
        expediente_instance = SL_Expedientes.objects.create(**expediente_data)

        preadmision_data = {
            'fk_derivacion': form.cleaned_data['fk_derivacion'],
            'fk_expediente': expediente_instance,
            'fk_legajo': form.cleaned_data['fk_legajo'],
            'organismo': form.cleaned_data['organismo'],
            'motivo_ingreso': form.cleaned_data['motivo_ingreso'],
            'obs_vulneracion': form.cleaned_data['obs_vulneracion'],
            'dinamica_familiar': form.cleaned_data['dinamica_familiar'],
            'conocimiento_situacion': form.cleaned_data['conocimiento_situacion'],
            'estado': "En proceso",
        }
        preadmi_instance = SL_PreAdmision.objects.create(**preadmision_data)

        fk_externo = form.cleaned_data.get('fk_externo')
        fk_legajo_referente = form.cleaned_data.get('fk_legajo_referente')
    
        if fk_externo:
            for externo in fk_externo.all():
                SL_Referentes.objects.create(fk_expediente=expediente_instance, fk_externo=externo)

        if fk_legajo_referente:
            for referente in fk_legajo_referente:
                SL_Referentes.objects.create(fk_expediente=expediente_instance, fk_legajo_referente=referente)
                
        # Procesar la carga de alarmas
        alarmas = form.cleaned_data.get('fk_alarmas')
        if alarmas:
            for alarma in alarmas:
                SL_Alarmas.objects.create(fk_expediente=expediente_instance, fk_alarmas_id=alarma.id)
        
        # Procesar la carga de grupo familiar
        familiares = form.cleaned_data.get('fk_legajo_familiar')
        if familiares:
            for familiar in familiares:
                SL_GrupoFamiliar.objects.create(fk_expediente=expediente_instance, fk_legajo_familiar=familiar)
        
        # Procesar la carga de archivos
        archivos = self.request.FILES.getlist('archivos')
        if archivos:
            for archivo in archivos:
                print ("==========================================")
                print(archivo)
                SL_ExpedientesArchivos.objects.create(fk_expediente=expediente_instance, archivo=archivo)

        base = LegajosDerivaciones.objects.get(pk=pk)
        base.estado = "Aceptada"
        base.save() 
        
        return redirect('SL_preadmisiones_ver', pk=preadmi_instance.pk)
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)   


class SLPreAdmisionesUpdateView(PermisosMixin,UpdateView, SuccessMessageMixin):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_SL/preadmisiones_form.html"
    model = SL_PreAdmision
    form_class = SL_MultiModelForm
    success_message = "Preadmisión creada correctamente"

    def get_context_data(self, **kwargs):
        pk = SL_PreAdmision.objects.filter(pk=self.kwargs["pk"]).first()
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(pk=pk.fk_derivacion_id).first()
        familia = LegajoGrupoFamiliar.objects.filter(fk_legajo_2_id=legajo.fk_legajo_id)
        familia_inversa = LegajoGrupoFamiliar.objects.filter(fk_legajo_1_id=legajo.fk_legajo_id)

        context["pk"] = pk.fk_derivacion_id
        context["legajo"] = legajo
        context["familia"] = familia
        context["familia_inversa"] = familia_inversa
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('detalle_expediente', kwargs={'pk': self.object.pk})
    

class SLPreAdmisionesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_SL/preadmisiones_list.html"
    model = SL_PreAdmision

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pre_admi = SL_PreAdmision.objects.all()
        context["object"] = pre_admi
        return context

class SLPreAdmisionesBuscarListView(PermisosMixin, TemplateView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_SL/preadmisiones_buscar.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        object_list = SL_PreAdmision.objects.none()
        mostrar_resultados = False
        mostrar_btn_resetear = False
        query = self.request.GET.get("busqueda")
        if query:
            object_list = SL_PreAdmision.objects.filter(Q(fk_legajo__apellido__iexact=query) | Q(fk_legajo__documento__iexact=query), fk_derivacion__fk_programa_id=25).exclude(estado__in=['Rechazada','Aceptada']).distinct()
            #object_list = Legajos.objects.filter(Q(apellido__iexact=query) | Q(documento__iexact=query))
            if not object_list:
                messages.warning(self.request, ("La búsqueda no arrojó resultados."))

            mostrar_btn_resetear = True
            mostrar_resultados = True

        context["mostrar_resultados"] = mostrar_resultados
        context["mostrar_btn_resetear"] = mostrar_btn_resetear
        context["object_list"] = object_list

        return self.render_to_response(context)

class SLPreAdmisionesDeleteView(PermisosMixin, DeleteView):
    permission_required = "Usuarios.rol_admin"
    model = SL_PreAdmision
    template_name = "SIF_SL/preadmisiones_confirm_delete.html"
    success_url = reverse_lazy("SL_preadmisiones_listar")

    def form_valid(self, form):
        if self.object.estado != "En proceso":
            messages.error(
                self.request,
                "No es posible eliminar una solicitud en estado " + self.object.estado,
            )

            return redirect("SL_preadmisiones_ver", pk=int(self.object.id))

        if self.request.user.id != self.object.creado_por.id:
            print(self.request.user)
            print(self.object.creado_por)
            messages.error(
                self.request,
                "Solo el usuario que generó esta derivación puede eliminarla.",
            )

            return redirect("SL_preadmisiones_ver", pk=int(self.object.id))

        else:
            self.object.delete()
            return redirect(self.success_url)

        
class SLIndiceVulneracionCreateView(PermisosMixin, CreateView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_SL/indiceingreso_form.html"
    form_class = SL_IndiceVulnerabilidadForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk=self.kwargs["pk"]
        object = SL_PreAdmision.objects.filter(pk=pk).first
        criterio = SL_IndicesVulnerabilidad.objects.all()
        context["object"] = object
        context["criterio"] = criterio
        return context
    
    def post(self, request, *args, **kwargs):
        pk=self.kwargs["pk"]
        preadmi = SL_PreAdmision.objects.filter(pk=pk).first()
        nombres_campos = request.POST.keys()

        for f in nombres_campos:
            if f.isdigit():
                base = SL_IndiceVulnerabilidad()
                base.fk_expediente_id = preadmi.fk_expediente.id
                base.fk_indice_id = f
                base.fk_legajo_id = preadmi.fk_legajo_id
                base.fk_preadmi_id = preadmi.pk
                base.creado_por_id = self.request.user.id
                base.save()
        
        if len(nombres_campos) > 1:
            preadmi.estado = "A efectivizar"
            preadmi.save()

        return redirect('SL_preadmisiones_ver', preadmi.id)
    
class SLIndiceVulneracionUpdateView (PermisosMixin, UpdateView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_SL/indiceingreso_form.html"
    model = SL_PreAdmision
    form_class = SL_IndiceVulnerabilidadForm

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        activos = SL_IndiceVulnerabilidad.objects.filter(fk_preadmi_id=pk)
        criterio = SL_IndicesVulnerabilidad.objects.all()

        context = super().get_context_data(**kwargs)
        context["object"] = SL_PreAdmision.objects.filter(pk=pk).first()
        context["activos"] = activos
        context["criterio"] = criterio
        return context
    
    def post(self, request, *args, **kwargs):
        pk=self.kwargs["pk"]
        preadmi = SL_PreAdmision.objects.filter(pk=pk).first()
        borrar = SL_IndiceVulnerabilidad.objects.filter(Q(fk_preadmi_id=pk) | Q(fk_expediente_id=preadmi.fk_expediente_id))
        borrar.delete()
        nombres_campos = request.POST.keys()

        for f in nombres_campos:
            if f.isdigit():
                base = SL_IndiceVulnerabilidad()
                base.fk_expediente_id = preadmi.fk_expediente.id
                base.fk_indice_id = f
                base.fk_legajo_id = preadmi.fk_legajo_id
                base.fk_preadmi_id = preadmi.pk
                base.creado_por_id = self.request.user.id
                base.save()

        return redirect('SL_preadmisiones_ver', preadmi.id)
    


class SLAdmisionesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_SL/adminsiones_list.html"
    model = SL_Admision

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        criterio_ingreso = SL_IndiceVulnerabilidad.objects.all()
        admi = SL_Admision.objects.all()
        conteo = SL_IndiceVulnerabilidad.objects.values('fk_preadmi_id').annotate(total=Count('fk_preadmi_id'))

        context ["conteo"] = conteo
        context["admi"] = admi
        context["foto_ingreso"] = criterio_ingreso.aggregate(total=Count('fk_criterios_ingreso'))
        context["puntaje_ingreso"] = criterio_ingreso.aggregate(total=Sum('fk_criterios_ingreso__puntaje'))
        return context

class SLAdmisionesDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.rol_admin"
    model = SL_Admision
    template_name = 'SIF_SL/admisiones_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk=self.kwargs["pk"]
        preadmi = SL_Admision.objects.filter(pk=pk).first()
        criterio = SL_IndiceVulnerabilidad.objects.filter(fk_preadmi_id=preadmi.fk_preadmi_id, fk_expediente_id=preadmi.fk_expediente_id)
        referentes = SL_Referentes.objects.filter(fk_expediente_id=preadmi.fk_expediente_id)
        grupo_familiar = SL_GrupoFamiliar.objects.filter(fk_expediente_id=preadmi.fk_expediente_id)
        equipo = SL_EquipoDesignado.objects.filter(fk_expediente_id=preadmi.fk_expediente_id).last()
        archivos = SL_ExpedientesArchivos.objects.filter(fk_expediente_id=preadmi.fk_expediente_id)
        resultado = SL_IndiceVulnerabilidad.objects.filter(Q(fk_preadmi_id=preadmi.fk_preadmi_id) | Q(fk_expediente_id=preadmi.fk_expediente_id))
        intervenciones = SL_Intervenciones.objects.filter(fk_admision_id=preadmi.id).all()

        context["mod_puntaje"] = criterio.aggregate(total=Sum('fk_indice__puntaje'))
        context["referentes"] = referentes
        context["grupo_familiar"] = grupo_familiar
        context["equipo"] = equipo
        context["archivos"] = archivos
        context['resultado'] = resultado.aggregate(total=Sum('fk_indice__puntaje'))
        context["intervenciones"] = intervenciones
        context["intervenciones_count"] = intervenciones.count()
        
        return context


#
#class SLInactivaAdmisionDetail(PermisosMixin, DetailView):
#    permission_required = "Usuarios.rol_admin"
#    template_name = "SIF_SL/inactiva_admisiones_detail.html"
#    model = SL_Admision
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        admi = SL_Admision.objects.filter(pk=self.kwargs["pk"]).first()
#
#        preadmi = SL_PreAdmision.objects.filter(pk=admi.fk_preadmi_id).first()
#        criterio = SL_IndiceIVI.objects.filter(fk_preadmi_id=preadmi, tipo="Egreso")
#        intervenciones = SL_Intervenciones.objects.filter(fk_admision_id=admi.id).all()
#        intervenciones_last = SL_Intervenciones.objects.filter(fk_admision_id=admi.id).last()
#        foto_ivi_fin = SL_Foto_IVI.objects.filter(fk_preadmi_id=admi.fk_preadmi_id, tipo="Egreso").first()
#        foto_ivi_inicio = SL_Foto_IVI.objects.filter(fk_preadmi_id=admi.fk_preadmi_id, tipo="Ingreso").first()
#
#        
#        context["foto_ivi_fin"] = foto_ivi_fin
#        context["foto_ivi_inicio"] = foto_ivi_inicio
#        context["criterio"] = criterio
#        context["object"] = admi
#        context["vo"] = self.object
#        context["intervenciones_count"] = intervenciones.count()
#        context["intervenciones_last"] = intervenciones_last
#        
#        return context



class SLIntervencionesCreateView(PermisosMixin, CreateView):
    permission_required = "Usuarios.rol_admin"
    model = SL_Intervenciones  # Debería ser el modelo SL_Intervenciones
    template_name = "SIF_SL/intervenciones_form.html"
    form_class = SL_IntervencionesForm

    def form_valid(self, form):
        form.instance.fk_admision_id = self.kwargs["pk"]
        form.instance.creado_por_id = self.request.user.id
        self.object = form.save()

        return redirect('SL_intervencion_ver', pk=self.object.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = SL_Admision.objects.get(pk=self.kwargs["pk"])  # Obtén el objeto directamente
        context["form"] = self.get_form()  # Obtiene una instancia del formulario

        return context
    
class SLIntervencionesUpdateView(PermisosMixin, UpdateView):
    permission_required = "Usuarios.rol_admin"
    model = SL_Intervenciones
    template_name = "SIF_SL/intervenciones_form.html"
    form_class = SL_IntervencionesForm

    def form_valid(self, form):
            pk = SL_Intervenciones.objects.filter(pk=self.kwargs["pk"]).first()
            admi = SL_Admision.objects.filter(id=pk.fk_admision.id).last()
            form.instance.fk_admision_id = admi.id
            form.instance.modificado_por_id = self.request.user.id
            self.object = form.save()

            return redirect('SL_admisiones_ver', self.object.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = SL_Intervenciones.objects.filter(pk=self.kwargs["pk"]).first()
        admi = SL_Admision.objects.filter(id=pk.fk_admision.id).first()

        context["object"] = admi

        return context

#class SLIntervencionesLegajosListView(PermisosMixin, DetailView):
#    permission_required = "Usuarios.rol_admin"
#    template_name = "SIF_SL/intervenciones_legajo_list.html"
#    model = SL_Admision
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        admi = SL_Admision.objects.filter(pk=self.kwargs["pk"]).first()
#        intervenciones = SL_Intervenciones.objects.filter(fk_admision_id=admi.id).all()
#        intervenciones_last = SL_Intervenciones.objects.filter(fk_admision_id=admi.id).last()
#        preadmi = SL_PreAdmision.objects.filter(pk=admi.fk_preadmi_id).first()
#        criterio = SL_IndiceIVI.objects.filter(fk_preadmi_id=preadmi, tipo="Ingreso")
#        observaciones = SL_Foto_IVI.objects.filter(clave=criterio.first().clave, tipo="Ingreso").first()
#        criterio2 = SL_IndiceIVI.objects.filter(fk_preadmi_id=preadmi, tipo="Ingreso")
#        observaciones2 = SL_Foto_IVI.objects.filter(clave=criterio2.last().clave, tipo="Ingreso").first()
#
#        context["object"] = admi
#        context["intervenciones"] = intervenciones
#        context["intervenciones_count"] = intervenciones.count()
#        context["intervenciones_last"] = intervenciones_last
#
#        context["puntaje"] = criterio.aggregate(total=Sum('fk_criterios_ivi__puntaje'))
#        context["observaciones"] = observaciones
#        context["observaciones2"] = observaciones2
#        context["puntaje2"] = criterio2.aggregate(total=Sum('fk_criterios_ivi__puntaje'))
#
#        return context
    
class SLIntervencionesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_SL/intervenciones_list.html"
    model = SL_Intervenciones

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        intervenciones = SL_Intervenciones.objects.all()
        context["intervenciones"] = intervenciones
        return context

class SLIntervencionesDetail (PermisosMixin, DetailView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_SL/intervencion_detail.html"
    model = SL_Intervenciones

class SLOpcionesResponsablesCreateView(PermisosMixin, CreateView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_SL/intervenciones_resposables.html"
    model = OpcionesResponsables
    form_class = SL_OpcionesResponsablesForm

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse('SL_OpcionesResponsables'))

class SLIntervencionesDeleteView(PermisosMixin, DeleteView):
    permission_required = "Usuarios.rol_admin"
    model = SL_Intervenciones
    template_name = "SIF_SL/intervenciones_confirm_delete.html"
    success_url = reverse_lazy("SL_intervenciones_listar")

    def form_valid(self, form):

        if self.request.user.id != self.object.creado_por.id:
            print(self.request.user)
            print(self.object.creado_por)
            messages.error(
                self.request,
                "Solo el usuario que generó esta derivación puede eliminarla.",
            )

            return redirect("SL_preadmisiones_ver", pk=int(self.object.id))

        else:
            self.object.delete()
            return redirect(self.success_url)
        

class SLAdmisionesBuscarListView(PermisosMixin, TemplateView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_SL/admisiones_buscar.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        object_list = SL_PreAdmision.objects.none()
        mostrar_resultados = False
        mostrar_btn_resetear = False
        query = self.request.GET.get("busqueda")
        if query:
            object_list = SL_Admision.objects.filter(Q(fk_preadmi__fk_legajo__apellido__iexact=query) | Q(fk_preadmi__fk_legajo__documento__iexact=query), fk_preadmi__fk_derivacion__fk_programa_id=25).exclude(estado__in=['Rechazada','Aceptada']).distinct()
            if not object_list:
                messages.warning(self.request, ("La búsqueda no arrojó resultados."))

            mostrar_btn_resetear = True
            mostrar_resultados = True

        context["mostrar_resultados"] = mostrar_resultados
        context["mostrar_btn_resetear"] = mostrar_btn_resetear
        context["object_list"] = object_list

        return self.render_to_response(context)
    
#class SLIndiceIviEgresoCreateView (PermisosMixin, CreateView):
#    permission_required = "Usuarios.rol_admin"
#    model = Legajos
#    template_name = "SIF_SL/indiceivi_form_egreso.html"
#    form_class = SL_IndiceIviForm
#    success_url = reverse_lazy("legajos_listar")
#    
#    
#    def get_context_data(self, **kwargs):
#        pk=self.kwargs["pk"]
#        context = super().get_context_data(**kwargs)
#        admi = SL_Admision.objects.filter(pk=pk).first()
#        object = Legajos.objects.filter(pk=admi.fk_preadmi.fk_legajo.id).first()
#        criterio = Criterios_IVI.objects.all()
#        context["object"] = object
#        context["criterio"] = criterio
#        context['form2'] = SL_IndiceIviHistorialForm()
#        context['admi'] = admi
#        return context
#    
#    def post(self, request, *args, **kwargs):
#        pk=self.kwargs["pk"]
#        admi = SL_Admision.objects.filter(pk=pk).first()
#        # Genera una clave única utilizando uuid4 (versión aleatoria)
#        preadmi = SL_PreAdmision.objects.filter(fk_legajo_id=admi.fk_preadmi.fk_legajo.id).first()
#        foto_ivi = SL_Foto_IVI.objects.filter(fk_preadmi_id=preadmi.id).first()
#        clave = foto_ivi.clave
#        nombres_campos = request.POST.keys()
#        puntaje_maximo = Criterios_IVI.objects.aggregate(total=Sum('puntaje'))['total']
#        total_puntaje = 0
#        for f in nombres_campos:
#            if f.isdigit():
#                criterio_ivi = Criterios_IVI.objects.filter(id=f).first()
#                # Sumar el valor de f al total_puntaje
#                total_puntaje += int(criterio_ivi.puntaje)
#                base = SL_IndiceIVI()
#                base.fk_criterios_ivi_id = f
#                base.fk_legajo_id = admi.fk_preadmi.fk_legajo.id
#                base.fk_preadmi_id = preadmi.id
#                base.tipo = "Egreso"
#                base.presencia = True
#                base.programa = "SL"
#                base.clave = clave
#                base.save()
#
#        # total_puntaje contiene la suma de los valores de F
#        foto = SL_Foto_IVI()
#        foto.observaciones = request.POST.get('observaciones', '')
#        foto.fk_preadmi_id = preadmi.id
#        foto.fk_legajo_id = preadmi.fk_legajo_id
#        foto.puntaje = total_puntaje
#        foto.puntaje_max = puntaje_maximo
#        #foto.crit_modificables = crit_modificables
#        #foto.crit_presentes = crit_presentes
#        foto.tipo = "Egreso"
#        foto.clave = clave
#        foto.creado_por_id = self.request.user.id
#        foto.save()
#
#        admi.estado = "Inactiva"
#        admi.modificado_por_id = self.request.user.id
#        admi.save()
#
#        #---------HISTORIAL---------------------------------
#        pk=self.kwargs["pk"]
#        legajo = admi.fk_preadmi
#        base = SL_Historial()
#        base.fk_legajo_id = legajo.fk_legajo.id
#        base.fk_legajo_derivacion_id = legajo.fk_derivacion_id
#        base.fk_preadmi_id = legajo.id
#        base.movimiento = "IVI EGRESO"
#        base.creado_por_id = self.request.user.id
#        base.save()
#
#        return redirect('SL_admisiones_listar')
    
class SLPreAdmisionesDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_SL/preadmisiones_detail.html"
    model = SL_PreAdmision

    def get_context_data(self, **kwargs):
        pk=self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        preadmi = SL_PreAdmision.objects.filter(pk=pk).first()
        resultado = SL_IndiceVulnerabilidad.objects.filter(Q(fk_preadmi_id=pk) | Q(fk_expediente_id=preadmi.fk_expediente_id))

        context['resultado'] = resultado.aggregate(total=Sum('fk_indice__puntaje'))
        return context

class SLExpedientesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.rol_admin"
    
    # Funcion de busqueda

    def get_queryset(self):
        query = self.request.GET.get('busqueda')

        if query:
            object_list = self.model.objects.filter(Q(expediente__icontains=query)).distinct()

        else:
            object_list = self.model.objects.all()

        return object_list
    
class SLDesignarEquipoCreateView(PermisosMixin, CreateView):
    permission_required = "Usuarios.rol_admin"
    model = SL_PreAdmision
    template_name = "SIF_SL/designarequipo_form.html"
    form_class = SL_EquipoDesignadoForm

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        preadmi = SL_PreAdmision.objects.filter(pk=pk).first()
        admision = SL_Admision()
        admision.fk_expediente_id = preadmi.fk_expediente_id
        admision.fk_preadmi_id = pk
        admision.estado = "Aceptado"
        admision.save()

        form.instance.creado_por_id = self.request.user.id
        form.instance.admi
        self.object = form.save()

        preadmi.estado = "Finalizado"
        preadmi.save()

        return redirect('SL_admisiones_ver', pk=admision.pk)
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = SL_PreAdmision.objects.get(pk=self.kwargs["pk"])
        return context

class SLDesignarEquipoUpdateView(PermisosMixin, UpdateView):
    permission_required = "Usuarios.rol_admin"
    model = SL_EquipoDesignado
    template_name = "SIF_SL/designarequipo_form.html"
    form_class = SL_EquipoDesignadoForm

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        preadmi = form.cleaned_data['fk_preadmi']
        expediente = form.cleaned_data['fk_expediente']
        admision = SL_Admision.objects.filter(fk_preadmi_id = preadmi, fk_expediente_id = expediente).last()
        form.instance.modificado_por_id = self.request.user.id
        self.object = form.save()
        
        return redirect('SL_admisiones_ver', pk=admision.pk)
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = SL_EquipoDesignado.objects.get(pk=self.kwargs["pk"])
        context["object"] = object.fk_preadmi
        return context
    
class SL_EquiposDesignadosDetailView(PermisosMixin, DetailView):
    permission_required = ['Usuarios.rol_admin','Usuarios.rol_observador','Usuarios.rol_consultante']
    template_name = "SIF_SL/sl_equipodesignado_detail.html"
    model = SL_Equipos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipo = SL_EquipoDesignado.objects.filter(fk_equipo_id=self.kwargs["pk"])
        context["equipo"] = equipo
        return context


class SL_EquiposDesignadosListView(PermisosMixin, ListView):
    permission_required = ['Usuarios.rol_admin','Usuarios.rol_observador','Usuarios.rol_consultante']
    queryset = SL_EquipoDesignado.objects.select_related('fk_equipo').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtenemos el nombre del equipo, su id y la cantidad de registros por cada equipo
        context['info_por_equipo'] = SL_EquipoDesignado.objects.values('fk_equipo__nombre', 'fk_equipo').annotate(cantidad=Count('id'))
        return context

