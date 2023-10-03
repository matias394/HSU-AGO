from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView,TemplateView
from Legajos.models import LegajosDerivaciones
from django.db.models import Q
from .models import *
from Configuraciones.models import *
from .forms import *
from Usuarios.mixins import PermisosMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.db.models import Sum
# # Create your views here.
#derivaciones = LegajosDerivaciones.objects.filter(m2m_programas__nombr__iexact="CDIF")
#print(derivaciones)

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
        context["analisis"] = model.filter(estado="En análisis")
        context["rechazadas"] = model.filter(estado="Rechazadas")
        context["enviadas"] = model.filter(fk_usuario=self.request.user)
        return context

class CDIFDerivacionesDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/derivaciones_detail.html"
    model = LegajosDerivaciones

class CDIFPreAdmisionesCreateView(PermisosMixin,CreateView, SuccessMessageMixin):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/preadmisiones_form.html"
    model = CDIF_PreAdmisiones
    form_class = CDIF_PreadmisionesForm
    success_message = "Preadmisión creada correctamente"

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(pk=pk).first()
        familia = LegajoGrupoFamiliar.objects.filter(fk_legajo_2_id=legajo.fk_legajo_id)
        centros = Organismos.objects.filter(nombre__startswith='CDIF')
        context["pk"] = pk
        context["legajo"] = legajo
        context["familia"] = familia
        context["centros"] = centros
        return context

    def form_valid(self, form):
        form.instance.estado = 'En proceso'
        form.instance.creado_por_id = self.request.user.id
        self.object = form.save()

        return HttpResponseRedirect(reverse('CDIF_preadmisiones_ver', args=[self.object.pk]))

class CDIFPreAdmisionesUpdateView(PermisosMixin,UpdateView, SuccessMessageMixin):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/preadmisiones_form.html"
    model = CDIF_PreAdmisiones
    form_class = CDIF_PreadmisionesForm
    success_message = "Preadmisión creada correctamente"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        pk = CDIF_PreAdmisiones.objects.filter(pk=self.kwargs["pk"]).first()
        legajo = LegajosDerivaciones.objects.filter(pk=pk.fk_derivacion_id).first()
        filtro = LegajoGrupoFamiliar.objects.filter(fk_legajo_2_id=legajo.fk_legajo_id)
        form.fields['fk_legajo_1'].queryset = filtro
        return form

    def get_context_data(self, **kwargs):
        pk = CDIF_PreAdmisiones.objects.filter(pk=self.kwargs["pk"]).first()
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(pk=pk.fk_derivacion_id).first()
        familia = LegajoGrupoFamiliar.objects.filter(fk_legajo_2_id=legajo.fk_legajo_id)
        centros = Organismos.objects.filter(nombre__startswith='CDIF')
        context["pk"] = pk.fk_derivacion_id
        context["legajo"] = legajo
        context["familia"] = familia
        context["centros"] = centros
        return context

    def form_valid(self, form):
        form.instance.estado = 'En proceso'
        self.object = form.save()

        return HttpResponseRedirect(reverse('CDIF_preadmisiones_ver', args=[self.object.pk]))

    #def form_invalid(self, form):
    #    errors = form.errors
    #    print(errors)
    #    return super().form_invalid(form)

class CDIFPreAdmisionesDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/preadmisiones_detail.html"
    model = CDIF_PreAdmisiones

    def get_context_data(self, **kwargs):
        pk = CDIF_PreAdmisiones.objects.filter(pk=self.kwargs["pk"]).first()
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(pk=pk.fk_derivacion_id).first()
        context["legajo"] = legajo
        return context
    
    def post(self, request, *args, **kwargs):
        if 'finalizar_preadm' in request.POST:
            # Realiza la actualización del campo aquí
            objeto = self.get_object()
            objeto.estado = 'Finalizada'
            objeto.save()
            
            # Redirige de nuevo a la vista de detalle actualizada
            return HttpResponseRedirect(self.request.path_info)

class CDIFPreAdmisionesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/preadmisiones_list.html"
    model = CDIF_PreAdmisiones

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pre_admi = CDIF_PreAdmisiones.objects.all()
        context["object"] = pre_admi
        return context

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
    model = CDIF_IndiceIVI
    template_name = "SIF_CDIF/indiceivi_form.html"
    form_class = CDIF_IndiceIviForm
    
    def get_context_data(self, **kwargs):
        pk=self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        object = CDIF_PreAdmisiones.objects.filter(pk=pk).first()
        criterio = Criterios_IVI.objects.all()
        context["object"] = object
        context["criterio"] = criterio
        context['form2'] = CDIF_IndiceIviObservForm()
        return context
    
    def post(self, request, *args, **kwargs):
        # Realiza la actualización del campo aquí
        pk=self.kwargs["pk"]
        preadm = CDIF_PreAdmisiones.objects.filter(pk=pk).first()
        form = self.request.POST
        for f in form:
            if f != 'observaciones':
                if f != 'csrfmiddlewaretoken':
                    base = CDIF_IndiceIVI()
                    base.fk_criterios_ivi_id = f
                    base.fk_preadmicion_id = preadm.id
                    base.presencia = True
                    base.save()
            if f == 'observaciones':
                if f != 'csrfmiddlewaretoken':
                    base2 = CDIF_IndiceIVI_Observ()
                    base2.observaciones = request.POST['observaciones']
                    base2.fk_preadmicion_id = preadm.id
                    base2.save()

        return HttpResponseRedirect(reverse('CDIF_indiceivi_ver', preadm.id))

    #def form_invalid(self, form):
    #    errors = form.errors
    #    print(errors)
    #    return super().form_invalid(form)   

class CDIFIndiceIviUpdateView (PermisosMixin, UpdateView):
    permission_required = "Usuarios.rol_admin"
    model = CDIF_PreAdmisiones
    template_name = "SIF_CDIF/indiceivi_form.html"
    form_class = CDIF_IndiceIviForm

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        context["object"] = CDIF_PreAdmisiones.objects.filter(pk=pk).first()
        context["criterio"] = Criterios_IVI.objects.all()
        context['form2'] = CDIF_IndiceIviObservForm()
        return context
    
    #def get_context_data(self, **kwargs):
    #    pk=self.kwargs["pk"]
    #    context = super().get_context_data(**kwargs)
    #    object = CDIF_PreAdmisiones.objects.filter(pk=pk).first()
    #    criterio = Criterios_IVI.objects.all()
    #    context["object"] = object
    #    context["criterio"] = criterio
    #    context['form2'] = CDIF_IndiceIviObservForm()
    #    return context
    
    def post(self, request, *args, **kwargs):
        # Realiza la actualización del campo aquí
        pk=self.kwargs["pk"]
        preadm = CDIF_PreAdmisiones.objects.filter(pk=pk).first()
        form = self.request.POST
        for f in form:
            if f != 'observaciones':
                if f != 'csrfmiddlewaretoken':
                    base = CDIF_IndiceIVI()
                    base.fk_criterios_ivi_id = f
                    base.fk_preadmicion_id = preadm.id
                    base.presencia = True
                    base.save()
            if f == 'observaciones':
                if f != 'csrfmiddlewaretoken':
                    base2 = CDIF_IndiceIVI_Observ()
                    base2.observaciones = request.POST['observaciones']
                    base2.fk_preadmicion_id = preadm.id
                    base2.save()

        return HttpResponseRedirect(reverse('CDIF_indiceivi_ver', preadm.id))

    #def form_invalid(self, form):
    #    errors = form.errors
    #    print(errors)
    #    return super().form_invalid(form)   
    
    
class CDIFIndiceIviDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.rol_admin"
    template_name = "SIF_CDIF/indiceivi_detail.html"
    model = CDIF_PreAdmisiones

    def get_context_data(self, **kwargs):
        pk=self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        object = CDIF_PreAdmisiones.objects.filter(pk=pk).first()
        criterio = CDIF_IndiceIVI.objects.filter(fk_preadmicion_id=object.id)
        observaciones = CDIF_IndiceIVI_Observ.objects.filter(fk_preadmicion_id=object.id).first()
        context["object"] = object
        context["criterio"] = criterio
        context["observaciones"] = observaciones
        context["puntaje"] = criterio.aggregate(total=Sum('fk_criterios_ivi__puntaje'))
        context["cantidad"] = criterio.count()
        context["modificables"] = criterio.filter(fk_criterios_ivi__modificable='Si').count()
        context["mod_puntaje"] = criterio.filter(fk_criterios_ivi__modificable='Si').aggregate(total=Sum('fk_criterios_ivi__puntaje'))
        context["ajustes"] = criterio.filter(fk_criterios_ivi__tipo='Ajustes').count()
        context['maximo'] = Criterios_IVI.objects.all().aggregate(total=Sum('puntaje'))
        return context