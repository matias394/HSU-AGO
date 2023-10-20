from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView,TemplateView, FormView
from Legajos.models import LegajosDerivaciones
from Legajos.forms import DerivacionesRechazoForm
from django.db.models import Q
from .models import *
from Configuraciones.models import *
from .forms import *
from Usuarios.mixins import PermisosMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.db.models import Sum, F, ExpressionWrapper, IntegerField
import uuid
from django.shortcuts import redirect
from django.contrib import messages
# # Create your views here.
#derivaciones = LegajosDerivaciones.objects.filter(m2m_programas__nombr__iexact="CDIF")
#print(derivaciones)

class CDIFDerivacionesBuscarListView(TemplateView, PermisosMixin):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/derivaciones_buscar.html"

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
                    pk = o.id
                return redirect("legajos_ver", pk)

            if not object_list:
                messages.warning(self.request, ("La búsqueda no arrojó resultados."))

            mostrar_btn_resetear = True
            mostrar_resultados = True

        context["mostrar_resultados"] = mostrar_resultados
        context["mostrar_btn_resetear"] = mostrar_btn_resetear
        context["object_list"] = object_list

        return self.render_to_response(context)


class CDIFDerivacionesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/derivaciones_bandeja_list.html"
    queryset = LegajosDerivaciones.objects.filter(fk_programa=23)

    def get_context_data(self, **kwargs):
        context = super(CDIFDerivacionesListView, self).get_context_data(**kwargs)

        model = LegajosDerivaciones.objects.filter(fk_programa=23)

        context["todas"] = model
        context["pendientes"] = model.filter(estado="Pendiente")
        context["aceptadas"] = model.filter(estado="Aceptada")
        context["rechazadas"] = model.filter(estado="Rechazada")
        context["enviadas"] = model.filter(fk_usuario=self.request.user)
        return context

class CDIFDerivacionesDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/derivaciones_detail.html"
    model = LegajosDerivaciones

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(pk=pk, fk_programa=23).first()
        ivi = CDIF_IndiceIVI.objects.filter(fk_legajo_id=legajo.fk_legajo_id)
        resultado = ivi.values('clave', 'creado', 'programa').annotate(total=Sum('fk_criterios_ivi__puntaje')).order_by('-creado')
        context["pk"] = pk
        context["ivi"] = ivi
        context["resultado"] = resultado
        return context

class CDIFDerivacionesRechazo(PermisosMixin, CreateView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/derivaciones_rechazo.html"
    form_class = DerivacionesRechazoForm

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(pk=pk, fk_programa=23).first()
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
        return HttpResponseRedirect(reverse('CDIF_derivaciones_listar'))
    
    def form_invalid(self, form):
        return super().form_invalid(form)   
    
    def get_success_url(self):
        return reverse('CDIF_derivaciones_listar')

class CDIFPreAdmisionesCreateView(PermisosMixin,CreateView, SuccessMessageMixin):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/preadmisiones_form.html"
    model = CDIF_PreAdmision
    form_class = CDIF_PreadmisionesForm
    success_message = "Preadmisión creada correctamente"

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(pk=pk).first()
        familia = LegajoGrupoFamiliar.objects.filter(fk_legajo_2_id=legajo.fk_legajo_id)
        familia_inversa = LegajoGrupoFamiliar.objects.filter(fk_legajo_1_id=legajo.fk_legajo_id)
        centros = Vacantes.objects.filter(fk_programa_id=23)
        context["pk"] = pk
        context["legajo"] = legajo
        context["familia"] = familia
        context["familia_inversa"] = familia_inversa
        context["centros"] = centros
        return context

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        form.instance.estado = 'En proceso'
        form.instance.creado_por_id = self.request.user.id
        sala = form.cleaned_data['sala_postula']
        turno = form.cleaned_data['turno_postula']
        if sala == 'Bebe' and turno == 'Mañana':
            form.instance.sala_short = 'manianabb'
        elif sala == 'Bebe' and turno == 'Tarde':
            form.instance.sala_short = 'tardebb'
        elif sala == '2' and turno == 'Mañana':
            form.instance.sala_short = 'maniana2'
        elif sala == '2' and turno == 'Tarde':
            form.instance.sala_short = 'tarde2'
        elif sala == '3' and turno == 'Mañana':
            form.instance.sala_short = 'maniana3'
        elif sala == '3' and turno == 'Tarde':
            form.instance.sala_short = 'tarde3'
        self.object = form.save()

        base = LegajosDerivaciones.objects.get(pk=pk)
        base.estado = "Aceptada"
        base.save() 
        
        #---- Historial--------------
        legajo = LegajosDerivaciones.objects.filter(pk=pk).first()
        base = CDIF_Historial()
        base.fk_legajo_id = legajo.fk_legajo.id
        base.fk_legajo_derivacion_id = pk
        base.fk_preadmi_id = self.object.id
        base.movimiento = "ACEPTADO A PREADMISION"
        base.creado_por_id = self.request.user.id
        base.save()

        return HttpResponseRedirect(reverse('CDIF_preadmisiones_ver', args=[self.object.pk]))

class CDIFPreAdmisionesUpdateView(PermisosMixin,UpdateView, SuccessMessageMixin):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/preadmisiones_form.html"
    model = CDIF_PreAdmision
    form_class = CDIF_PreadmisionesForm
    success_message = "Preadmisión creada correctamente"

    def get_context_data(self, **kwargs):
        pk = CDIF_PreAdmision.objects.filter(pk=self.kwargs["pk"]).first()
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(pk=pk.fk_derivacion_id).first()
        familia = LegajoGrupoFamiliar.objects.filter(fk_legajo_2_id=legajo.fk_legajo_id)
        familia_inversa = LegajoGrupoFamiliar.objects.filter(fk_legajo_1_id=legajo.fk_legajo_id)
        centros = Vacantes.objects.filter(fk_programa_id=23)

        context["pk"] = pk.fk_derivacion_id
        context["legajo"] = legajo
        context["familia"] = familia
        context["familia_inversa"] = familia_inversa
        context["centros"] = centros
        return context

    def form_valid(self, form):
        pk = CDIF_PreAdmision.objects.filter(pk=self.kwargs["pk"]).first()
        form.instance.creado_por_id = pk.creado_por_id
        form.instance.estado = pk.estado
        form.instance.modificado_por_id = self.request.user.id
        self.object = form.save()

        return HttpResponseRedirect(reverse('CDIF_preadmisiones_ver', args=[self.object.pk]))

class CDIFPreAdmisionesDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/preadmisiones_detail.html"
    model = CDIF_PreAdmision

    def get_context_data(self, **kwargs):
        pk = CDIF_PreAdmision.objects.filter(pk=self.kwargs["pk"]).first()
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(pk=pk.fk_derivacion_id).first()
        familia = LegajoGrupoFamiliar.objects.filter(fk_legajo_2_id=legajo.fk_legajo_id)
        ivi = CDIF_IndiceIVI.objects.filter(fk_legajo_id=legajo.fk_legajo_id)
        resultado = ivi.values('clave', 'creado', 'programa').annotate(total=Sum('fk_criterios_ivi__puntaje')).order_by('-creado')
        context["ivi"] = ivi
        context["resultado"] = resultado
        context["legajo"] = legajo
        context["familia"] = familia
        return context
    
    def post(self, request, *args, **kwargs):
        if 'finalizar_preadm' in request.POST:
            # Realiza la actualización del campo aquí
            objeto = self.get_object()
            objeto.estado = 'Finalizada'
            objeto.save()

            #---------HISTORIAL---------------------------------
            pk=self.kwargs["pk"]
            legajo = CDIF_PreAdmision.objects.filter(pk=pk).first()
            base = CDIF_Historial()
            base.fk_legajo_id = legajo.fk_legajo.id
            base.fk_legajo_derivacion_id = legajo.fk_derivacion_id
            base.fk_preadmi_id = pk
            base.movimiento = "FINALIZADO PREADMISION"
            base.creado_por_id = self.request.user.id
            base.save()
            # Redirige de nuevo a la vista de detalle actualizada
            return HttpResponseRedirect(self.request.path_info)

class CDIFPreAdmisionesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/preadmisiones_list.html"
    model = CDIF_PreAdmision

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pre_admi = CDIF_PreAdmision.objects.all()
        context["object"] = pre_admi
        return context

class CDIFPreAdmisionesBuscarListView(PermisosMixin, TemplateView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/preadmisiones_buscar.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        object_list = LegajosDerivaciones.objects.none()
        mostrar_resultados = False
        mostrar_btn_resetear = False
        query = self.request.GET.get("busqueda")
        if query:
            object_list = LegajosDerivaciones.objects.filter(Q(fk_legajo__apellido__iexact=query) | Q(fk_legajo__documento__iexact=query), fk_programa_id=23).exclude(estado__in=['Rechazada','Aceptada']).distinct()
            if not object_list:
                messages.warning(self.request, ("La búsqueda no arrojó resultados."))

            mostrar_btn_resetear = True
            mostrar_resultados = True

        context["mostrar_resultados"] = mostrar_resultados
        context["mostrar_btn_resetear"] = mostrar_btn_resetear
        context["object_list"] = object_list

        return self.render_to_response(context)

class CDIFPreAdmisionesDeleteView(PermisosMixin, DeleteView):
    permission_required = "Usuarios.rol_admin"
    model = CDIF_PreAdmision
    template_name = "SIF_CDIF/preadmisiones_confirm_delete.html"
    success_url = reverse_lazy("CDIF_preadmisiones_listar")

    def form_valid(self, form):
        if self.object.estado != "En proceso":
            messages.error(
                self.request,
                "No es posible eliminar una solicitud en estado " + self.object.estado,
            )

            return redirect("CDIF_preadmisiones_ver", pk=int(self.object.id))

        if self.request.user.id != self.object.creado_por.id:
            print(self.request.user)
            print(self.object.creado_por)
            messages.error(
                self.request,
                "Solo el usuario que generó esta derivación puede eliminarla.",
            )

            return redirect("CDIF_preadmisiones_ver", pk=int(self.object.id))

        else:
            self.object.delete()
            return redirect(self.success_url)

class CDIFCriteriosIVICreateView(PermisosMixin, CreateView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/criterios_ivi_form.html"
    model = Criterios_IVI
    form_class = criterios_IVI

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse('CDIF_criterios_ivi_crear'))

 
class CDIFIndiceIviCreateView (PermisosMixin, CreateView):
    permission_required = "Usuarios.rol_admin"
    model = Legajos
    template_name = "SIF_CDIF/indiceivi_form.html"
    form_class = CDIF_IndiceIviForm
    success_url = reverse_lazy("legajos_listar")
    
    
    def get_context_data(self, **kwargs):
        pk=self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        object = Legajos.objects.filter(pk=pk).first()
        criterio = Criterios_IVI.objects.all()
        context["object"] = object
        context["criterio"] = criterio
        context['form2'] = CDIF_IndiceIviHistorialForm()
        return context
    
    def post(self, request, *args, **kwargs):
        pk=self.kwargs["pk"]
        # Genera una clave única utilizando uuid4 (versión aleatoria)
        derivacion = CDIF_PreAdmision.objects.filter(fk_legajo_id=pk).first()
        clave = str(uuid.uuid4())
        nombres_campos = request.POST.keys()
        for f in nombres_campos:
            if f.isdigit():
                base = CDIF_IndiceIVI()
                base.fk_criterios_ivi_id = f
                base.fk_legajo_id = pk
                base.fk_derivacion_id = derivacion.id
                base.presencia = True
                base.programa = "CDIF"
                base.clave = clave
                base.save()
            if f == 'observaciones':
                puntaje_maximo = Criterios_IVI.objects.aggregate(total=Sum('puntaje'))['total']
                base2 = CDIF_Historial_IVI()
                base2.observaciones = request.POST.get('observaciones', '')
                base2.programa = "CDIF"
                base2.puntaje_max = puntaje_maximo
                base2.creado_por_id = self.request.user.id
                base2.fk_legajo_id = pk
                base2.clave = clave
                base2.save()
        
        #---------HISTORIAL---------------------------------
        pk=self.kwargs["pk"]
        legajo = CDIF_PreAdmision.objects.filter(fk_legajo=pk).first()
        base = CDIF_Historial()
        base.fk_legajo_id = legajo.fk_legajo.id
        base.fk_legajo_derivacion_id = legajo.fk_derivacion_id
        base.fk_preadmi_id = legajo.id
        base.movimiento = "CREACION IVI"
        base.creado_por_id = self.request.user.id
        base.save()

        return redirect('CDIF_indiceivi_ver', derivacion.id)


class CDIFIndiceIviUpdateView (PermisosMixin, UpdateView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/indiceivi_edit.html"
    model = CDIF_PreAdmision
    form_class = CDIF_IndiceIviForm

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        activos = CDIF_IndiceIVI.objects.filter(fk_derivacion_id=pk)
        activos_first = activos.first()
        observaciones = CDIF_Historial_IVI.objects.filter(clave=activos_first.clave).first()

        context = super().get_context_data(**kwargs)
        context["object"] = CDIF_PreAdmision.objects.filter(pk=pk).first()
        context["activos"] = activos
        context["clave"] = observaciones.clave
        context["observaciones"] = observaciones.observaciones
        context["criterio"] = Criterios_IVI.objects.all()
        context['form2'] = CDIF_IndiceIviHistorialForm()
        return context
    
    def post(self, request, *args, **kwargs):
        pk=self.kwargs["pk"]
        # Genera una clave única utilizando uuid4 (versión aleatoria)
        derivacion = CDIF_PreAdmision.objects.filter(fk_legajo_id=pk).first()
        clave = request.POST['clave']
        nombres_campos = request.POST.keys()
        for f in nombres_campos:
            if f.isdigit():
                base = CDIF_IndiceIVI.objects.filter(clave=clave,fk_criterios_ivi_id = f)
                base.presencia = True
                #base.save()
            if f == 'observaciones':
                base2 = CDIF_Historial_IVI.objects.filter(clave=clave)
                base2.observaciones = request.POST['observaciones']
                #base2.save()

        return redirect('CDIF_indiceivi_ver', derivacion.id)

    #def form_invalid(self, form):
    #    errors = form.errors
    #    print(errors)
    #    return super().form_invalid(form)   
    
    
class CDIFIndiceIviDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/indiceivi_detail.html"
    model = CDIF_PreAdmision

    def get_context_data(self, **kwargs):
        pk=self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        criterio = CDIF_IndiceIVI.objects.filter(fk_derivacion_id=pk)
        object = CDIF_PreAdmision.objects.filter(pk=pk).first()
        observaciones = CDIF_Historial_IVI.objects.filter(clave=criterio.first().clave).first()

        context["object"] = object
        context["criterio"] = criterio
        context["observaciones"] = observaciones.observaciones
        context["puntaje"] = criterio.aggregate(total=Sum('fk_criterios_ivi__puntaje'))
        context["cantidad"] = criterio.count()
        context["modificables"] = criterio.filter(fk_criterios_ivi__modificable='Si').count()
        context["mod_puntaje"] = criterio.filter(fk_criterios_ivi__modificable='Si').aggregate(total=Sum('fk_criterios_ivi__puntaje'))
        context["ajustes"] = criterio.filter(fk_criterios_ivi__tipo='Ajustes').count()
        context['maximo'] = observaciones.puntaje_max
        return context
    
class CDIFPreAdmisiones3DetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/preadmisiones_detail3.html"
    model = CDIF_PreAdmision

    def get_context_data(self, **kwargs):
        pk = CDIF_PreAdmision.objects.filter(pk=self.kwargs["pk"]).first()
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(pk=pk.fk_derivacion_id).first()
        familia = LegajoGrupoFamiliar.objects.filter(fk_legajo_2_id=legajo.fk_legajo_id)
        criterio = CDIF_IndiceIVI.objects.filter(fk_derivacion_id=pk)
        observaciones = CDIF_Historial_IVI.objects.filter(clave=criterio.first().clave).first()

        context["legajo"] = legajo
        context["familia"] = familia
        context["observaciones"] = observaciones
        context["puntaje"] = criterio.aggregate(total=Sum('fk_criterios_ivi__puntaje'))
        context["cantidad"] = criterio.count()
        context["modificables"] = criterio.filter(fk_criterios_ivi__modificable='Si').count()
        context["mod_puntaje"] = criterio.filter(fk_criterios_ivi__modificable='Si').aggregate(total=Sum('fk_criterios_ivi__puntaje'))
        context["ajustes"] = criterio.filter(fk_criterios_ivi__tipo='Ajustes').count()
        context['maximo'] = observaciones.puntaje_max
        return context
    
    def post(self, request, *args, **kwargs):
        if 'admitir' in request.POST:
            preamd = CDIF_PreAdmision.objects.filter(pk=self.kwargs["pk"]).first()

            base1 = CDIF_Admision()
            base1.fk_preadmi_id = preamd.pk
            base1.estado_vacante = "Lista de espera"
            base1.creado_por_id = self.request.user.id
            base1.save()
            redirigir = base1.pk

            #---------HISTORIAL---------------------------------
            pk=self.kwargs["pk"]
            legajo = CDIF_PreAdmision.objects.filter(pk=pk).first()
            base = CDIF_Historial()
            base.fk_legajo_id = legajo.fk_legajo.id
            base.fk_legajo_derivacion_id = legajo.fk_derivacion_id
            base.fk_preadmi_id = pk
            base.fk_admision_id = redirigir
            base.movimiento = "ADMITIDO"
            base.creado_por_id = self.request.user.id
            base.save()

            # Redirige de nuevo a la vista de detalle actualizada
            return redirect('CDIF_admisiones_ver', redirigir)

class CDIFAdmisionesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/adminsiones_list.html"
    model = CDIF_Admision

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        criterio = CDIF_IndiceIVI.objects.all()
        admi = CDIF_Admision.objects.all()
        context["admi"] = admi
        context["puntaje"] = criterio.aggregate(total=Sum('fk_criterios_ivi__puntaje'))
        return context

class CDIFAdmisionesDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.rol_admin"
    model = CDIF_Admision
    template_name = 'SIF_CDIF/admisiones_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = CDIF_Admision.objects.filter(pk=self.kwargs["pk"]).first()
        preadmi = CDIF_PreAdmision.objects.filter(pk=pk.fk_preadmi_id).first()
        criterio = CDIF_IndiceIVI.objects.filter(fk_derivacion_id=preadmi)
        observaciones = CDIF_Historial_IVI.objects.filter(clave=criterio.first().clave).first()

        context["observaciones"] = observaciones
        context["puntaje"] = criterio.aggregate(total=Sum('fk_criterios_ivi__puntaje'))
        context["cantidad"] = criterio.count()
        context["modificables"] = criterio.filter(fk_criterios_ivi__modificable='Si').count()
        context["mod_puntaje"] = criterio.filter(fk_criterios_ivi__modificable='Si').aggregate(total=Sum('fk_criterios_ivi__puntaje'))
        context["ajustes"] = criterio.filter(fk_criterios_ivi__tipo='Ajustes').count()
        context['maximo'] = observaciones.puntaje_max
        
        return context

class CDIFVacantesAdmision(PermisosMixin, CreateView):
    permission_required = "Usuarios.rol_admin"
    model = CDIF_Admision
    template_name = "SIF_CDIF/vacantes_form.html"
    form_class = CDIF_VacantesOtorgadasForm

    def form_valid(self, form):
        sala = form.cleaned_data['sala']
        turno = form.cleaned_data['turno']
        if sala == 'Bebe' and turno == 'Mañana':
            form.instance.salashort = 'manianabb'
        elif sala == 'Bebe' and turno == 'Tarde':
            form.instance.salashort = 'tardebb'
        elif sala == '2' and turno == 'Mañana':
            form.instance.salashort = 'maniana2'
        elif sala == '2' and turno == 'Tarde':
            form.instance.salashort = 'tarde2'
        elif sala == '3' and turno == 'Mañana':
            form.instance.salashort = 'maniana3'
        elif sala == '3' and turno == 'Tarde':
            form.instance.salashort = 'tarde3'
        self.object = form.save()

        base1 = CDIF_Admision.objects.filter(pk=self.kwargs["pk"]).first()
        base1.estado_vacante = "Finalizada"
        base1.save()
        
        # --------- HISTORIAL ---------------------------------
        pk = self.kwargs["pk"]
        legajo = CDIF_Admision.objects.filter(pk=pk).first()
        base = CDIF_Historial()
        base.fk_legajo_id = legajo.fk_preadmi.fk_legajo.id
        base.fk_legajo_derivacion_id = legajo.fk_preadmi.fk_derivacion_id
        base.fk_preadmi_id = legajo.fk_preadmi.pk
        base.fk_admision_id = pk
        base.movimiento = "VACANTE OTORGADA"
        base.creado_por_id = self.request.user.id
        base.save()
        
        return redirect('CDIF_asignado_admisiones_ver', legajo.pk)

    def form_invalid(self, form):
        errors = form.errors
        print(errors)
        return super().form_invalid(form) 
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = CDIF_Admision.objects.filter(pk=self.kwargs["pk"]).first()

        preadmi = CDIF_PreAdmision.objects.filter(pk=pk.fk_preadmi_id).first()
        criterio = CDIF_IndiceIVI.objects.filter(fk_derivacion_id=preadmi)
        observaciones = CDIF_Historial_IVI.objects.filter(clave=criterio.first().clave).first()

        context["object"] = pk
        context["observaciones"] = observaciones
        context["puntaje"] = criterio.aggregate(total=Sum('fk_criterios_ivi__puntaje'))
        context["cantidad"] = criterio.count()
        context["modificables"] = criterio.filter(fk_criterios_ivi__modificable='Si').count()
        context["mod_puntaje"] = criterio.filter(fk_criterios_ivi__modificable='Si').aggregate(total=Sum('fk_criterios_ivi__puntaje'))
        context["ajustes"] = criterio.filter(fk_criterios_ivi__tipo='Ajustes').count()
        context['maximo'] = observaciones.puntaje_max
        
        return context

class CDIFVacantesAdmisionCambio(PermisosMixin, CreateView):
    permission_required = "Usuarios.rol_admin"
    model = CDIF_Admision
    template_name = "SIF_CDIF/vacantes_form_cambio.html"
    form_class = CDIF_VacantesOtorgadasForm

    def form_valid(self, form):
        if form.cleaned_data['fecha_egreso'] == None:
            messages.error(self.request, 'El campo fecha de egreso es requerido.')
            return super().form_invalid(form) 
        else:
            form.evento = "CambioVacante"
            sala = form.cleaned_data['sala']
            turno = form.cleaned_data['turno']
            if sala == 'Bebe' and turno == 'Mañana':
                form.instance.salashort = 'manianabb'
            elif sala == 'Bebe' and turno == 'Tarde':
                form.instance.salashort = 'tardebb'
            elif sala == '2' and turno == 'Mañana':
                form.instance.salashort = 'maniana2'
            elif sala == '2' and turno == 'Tarde':
                form.instance.salashort = 'tarde2'
            elif sala == '3' and turno == 'Mañana':
                form.instance.salashort = 'maniana3'
            elif sala == '3' and turno == 'Tarde':
                form.instance.salashort = 'tarde3'
            self.object = form.save()

        
            # --------- HISTORIAL ---------------------------------
            pk = self.kwargs["pk"]
            legajo = CDIF_Admision.objects.filter(pk=pk).first()
            base = CDIF_Historial()
            base.fk_legajo_id = legajo.fk_preadmi.fk_legajo.id
            base.fk_legajo_derivacion_id = legajo.fk_preadmi.fk_derivacion_id
            base.fk_preadmi_id = legajo.fk_preadmi.pk
            base.fk_admision_id = pk
            base.movimiento = "CAMBIO VACANTE"
            base.creado_por_id = self.request.user.id
            base.save()

        return redirect('CDIF_asignado_admisiones_ver', legajo.id)
    
    #def form_invalid(self, form):
    #    errors = form.errors
    #    print(errors)
    #    return super().form_invalid(form) 
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = CDIF_Admision.objects.filter(pk=self.kwargs["pk"]).first()
        vacante_otorgada = CDIF_VacantesOtorgadas.objects.filter(fk_admision_id=self.kwargs["pk"]).first()

        preadmi = CDIF_PreAdmision.objects.filter(pk=pk.fk_preadmi_id).first()
        criterio = CDIF_IndiceIVI.objects.filter(fk_derivacion_id=preadmi)
        observaciones = CDIF_Historial_IVI.objects.filter(clave=criterio.first().clave).first()

        context["object"] = pk
        context["observaciones"] = observaciones
        context["puntaje"] = criterio.aggregate(total=Sum('fk_criterios_ivi__puntaje'))
        context["cantidad"] = criterio.count()
        context["modificables"] = criterio.filter(fk_criterios_ivi__modificable='Si').count()
        context["mod_puntaje"] = criterio.filter(fk_criterios_ivi__modificable='Si').aggregate(total=Sum('fk_criterios_ivi__puntaje'))
        context["ajustes"] = criterio.filter(fk_criterios_ivi__tipo='Ajustes').count()
        context['maximo'] = observaciones.puntaje_max
        context["vo"] = vacante_otorgada
        
        return context

class CDIFAsignadoAdmisionDetail(PermisosMixin, DetailView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/asignado_admisiones_detail.html"
    model = CDIF_Admision

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        admi = CDIF_Admision.objects.filter(pk=self.kwargs["pk"]).first()

        preadmi = CDIF_PreAdmision.objects.filter(pk=admi.fk_preadmi_id).first()
        criterio = CDIF_IndiceIVI.objects.filter(fk_derivacion_id=preadmi)
        criterio2 = CDIF_IndiceIVI.objects.filter(fk_derivacion_id=preadmi)
        observaciones = CDIF_Historial_IVI.objects.filter(clave=criterio.first().clave).first()
        observaciones2 = CDIF_Historial_IVI.objects.filter(clave=criterio2.last().clave).first()
        lastVO = CDIF_VacantesOtorgadas.objects.filter(fk_admision_id=admi.id).last()
        movimientosVO =  CDIF_VacantesOtorgadas.objects.filter(fk_admision_id=admi.id).all()
        intervenciones = CDIF_Intervenciones.objects.filter(fk_admision_id=admi.id).all()
        intervenciones_last = CDIF_Intervenciones.objects.filter(fk_admision_id=admi.id).last()


        context["observaciones"] = observaciones
        context["observaciones2"] = observaciones2
        context["criterio"] = criterio
        context["puntaje"] = criterio.aggregate(total=Sum('fk_criterios_ivi__puntaje'))
        context["puntaje2"] = criterio2.aggregate(total=Sum('fk_criterios_ivi__puntaje'))
        context["object"] = admi
        context["vo"] = self.object
        context["lastvo"] = lastVO
        context["movimientosVO"] = movimientosVO
        context["intervenciones_count"] = intervenciones.count()
        context["intervenciones_last"] = intervenciones_last
        
        return context
    


class CDIFVacantesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.rol_admin"
    model = Vacantes
    template_name = 'SIF_CDIF/vacantes_list.html'
    context_object_name = 'organizaciones'
    
    def get_queryset(self):
        organizaciones = Vacantes.objects.values_list('nombre', flat=True).distinct()
        data = []

        for organizacion in organizaciones:
            organizacion_data = {'organizacion': organizacion}

            # Calcular la cantidad de vacantes por sala agrupadas
            for sala_group in [['manianabb', 'tardebb'], ['maniana2', 'tarde2'], ['maniana3', 'tarde3']]:
                total_vacantes = Vacantes.objects.filter(nombre=organizacion).aggregate(
                    total=Sum(F(sala_group[0]) + F(sala_group[1]))
                )['total'] or 0

                asignadas = CDIF_VacantesOtorgadas.objects.filter(
                    fk_organismo__nombre=organizacion,
                    salashort__in=sala_group
                ).count()

                disponibles = CDIF_Admision.objects.filter(
                    fk_preadmi__centro_postula__nombre=organizacion,
                    fk_preadmi__sala_short__in=sala_group,
                    estado_vacante='Lista de espera'
                ).count()

                organizacion_data['_'.join(sala_group) + '_total'] = total_vacantes
                organizacion_data['_'.join(sala_group) + '_asignadas'] = asignadas
                organizacion_data['_'.join(sala_group) + '_disponibles'] = disponibles

            # Calcular los totales de vacantes, asignadas y disponibles por organización
            total_vacantes_org = sum([organizacion_data['_'.join(sala_group) + '_total'] for sala_group in [['manianabb', 'tardebb'], ['maniana2', 'tarde2'], ['maniana3', 'tarde3']]])
            total_asignadas_org = sum([organizacion_data['_'.join(sala_group) + '_asignadas'] for sala_group in [['manianabb', 'tardebb'], ['maniana2', 'tarde2'], ['maniana3', 'tarde3']]])
            total_disponibles_org = sum([organizacion_data['_'.join(sala_group) + '_disponibles'] for sala_group in [['manianabb', 'tardebb'], ['maniana2', 'tarde2'], ['maniana3', 'tarde3']]])

            organizacion_data['total_vacantes'] = total_vacantes_org
            organizacion_data['total_asignadas'] = total_asignadas_org
            organizacion_data['total_disponibles'] = total_disponibles_org

            data.append(organizacion_data)

        return data
    
    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['organizaciones'] = self.get_queryset()
    #    print(context)
    #    return context
    
class CDIFVacantesDetailView (PermisosMixin, DetailView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/vacantes_detail.html"
    model = Vacantes

class CDIFIntervencionesCreateView(PermisosMixin, CreateView):
    permission_required = "Usuarios.rol_admin"
    model = CDIF_Intervenciones  # Debería ser el modelo CDIF_Intervenciones
    template_name = "SIF_CDIF/intervenciones_form.html"
    form_class = CDIF_IntervencionesForm

    def form_valid(self, form):
        form.instance.fk_admision_id = self.kwargs["pk"]
        form.instance.creado_por_id = self.request.user.id
        self.object = form.save()
        
        # --------- HISTORIAL ---------------------------------
        pk = self.kwargs["pk"]
        legajo = CDIF_Admision.objects.filter(pk=pk).first()
        base = CDIF_Historial()
        base.fk_legajo_id = legajo.fk_preadmi.fk_legajo.id
        base.fk_legajo_derivacion_id = legajo.fk_preadmi.fk_derivacion_id
        base.fk_preadmi_id = legajo.fk_preadmi.pk
        base.fk_admision_id = legajo.id  # Cambia a self.object.id
        base.movimiento = "INTERVENCION CREADA"
        base.creado_por_id = self.request.user.id
        base.save()

        return redirect('CDIF_intervencion_ver', pk=self.object.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = CDIF_Admision.objects.get(pk=self.kwargs["pk"])  # Obtén el objeto directamente
        context["form"] = self.get_form()  # Obtiene una instancia del formulario

        return context
    
class CDIFIntervencionesUpdateView(PermisosMixin, UpdateView):
    permission_required = "Usuarios.rol_admin"
    model = CDIF_Intervenciones
    template_name = "SIF_CDIF/intervenciones_form.html"
    form_class = CDIF_IntervencionesForm

    def form_valid(self, form):
            pk = CDIF_Intervenciones.objects.filter(pk=self.kwargs["pk"]).first()
            admi = CDIF_Admision.objects.filter(id=pk.fk_admision.id).first()
            form.instance.fk_admision_id = admi.id
            form.instance.modificado_por_id = self.request.user.id
            self.object = form.save()
        
            # --------- HISTORIAL ---------------------------------
            pk = self.kwargs["pk"]
            pk = CDIF_Intervenciones.objects.filter(pk=pk).first()
            legajo = CDIF_Admision.objects.filter(pk=pk.fk_admision_id).first()
            base = CDIF_Historial()
            base.fk_legajo_id = legajo.fk_preadmi.fk_legajo.id
            base.fk_legajo_derivacion_id = legajo.fk_preadmi.fk_derivacion_id
            base.fk_preadmi_id = legajo.fk_preadmi.pk
            base.fk_admision_id = legajo.pk
            base.movimiento = "INTERVENCION MODIFICADA"
            base.creado_por_id = self.request.user.id
            base.save()

            return redirect('CDIF_intervencion_ver', self.object.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = CDIF_Intervenciones.objects.filter(pk=self.kwargs["pk"]).first()
        admi = CDIF_Admision.objects.filter(id=pk.fk_admision.id).first()

        context["object"] = admi

        return context

class CDIFIntervencionesLegajosListView(PermisosMixin, DetailView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/intervenciones_legajo_list.html"
    model = CDIF_Admision

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        admi = CDIF_Admision.objects.filter(pk=self.kwargs["pk"]).first()
        lastVO = CDIF_VacantesOtorgadas.objects.filter(fk_admision_id=admi.id).last()
        intervenciones = CDIF_Intervenciones.objects.filter(fk_admision_id=admi.id).all()
        intervenciones_last = CDIF_Intervenciones.objects.filter(fk_admision_id=admi.id).last()
        preadmi = CDIF_PreAdmision.objects.filter(pk=admi.fk_preadmi_id).first()
        criterio = CDIF_IndiceIVI.objects.filter(fk_derivacion_id=preadmi)
        observaciones = CDIF_Historial_IVI.objects.filter(clave=criterio.first().clave).first()
        criterio2 = CDIF_IndiceIVI.objects.filter(fk_derivacion_id=preadmi)
        observaciones2 = CDIF_Historial_IVI.objects.filter(clave=criterio2.last().clave).first()

        context["object"] = admi
        context["lastvo"] = lastVO
        context["intervenciones"] = intervenciones
        context["intervenciones_count"] = intervenciones.count()
        context["intervenciones_last"] = intervenciones_last

        context["puntaje"] = criterio.aggregate(total=Sum('fk_criterios_ivi__puntaje'))
        context["observaciones"] = observaciones
        context["observaciones2"] = observaciones2
        context["puntaje2"] = criterio2.aggregate(total=Sum('fk_criterios_ivi__puntaje'))

        return context
    
class CDIFIntervencionesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/intervenciones_list.html"
    model = CDIF_Intervenciones

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        intervenciones = CDIF_Intervenciones.objects.all()
        context["intervenciones"] = intervenciones
        return context

class CDIFIntervencionesDetail (PermisosMixin, DetailView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/intervencion_detail.html"
    model = CDIF_Intervenciones

class CDIFOpcionesResponsablesCreateView(PermisosMixin, CreateView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/intervenciones_resposables.html"
    model = OpcionesResponsables
    form_class = CDIF_OpcionesResponsablesForm

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse('CDIF_OpcionesResponsables'))

class CDIFIntervencionesDeleteView(PermisosMixin, DeleteView):
    permission_required = "Usuarios.rol_admin"
    model = CDIF_Intervenciones
    template_name = "SIF_CDIF/intervenciones_confirm_delete.html"
    success_url = reverse_lazy("CDIF_intervenciones_listar")

    def form_valid(self, form):

        if self.request.user.id != self.object.creado_por.id:
            print(self.request.user)
            print(self.object.creado_por)
            messages.error(
                self.request,
                "Solo el usuario que generó esta derivación puede eliminarla.",
            )

            return redirect("CDIF_preadmisiones_ver", pk=int(self.object.id))

        else:
            self.object.delete()
            return redirect(self.success_url)