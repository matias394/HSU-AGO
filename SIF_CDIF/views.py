from django.forms import BaseModelForm
from django.forms.models import model_to_dict
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    TemplateView,
    FormView,
)
from django.http import JsonResponse
from Legajos.forms import DerivacionesRechazoForm, LegajosDerivacionesForm
from django.db.models import Q
from .models import *
from Configuraciones.models import *
from .forms import *
from Usuarios.mixins import PermisosMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.db.models import Sum, F, ExpressionWrapper, IntegerField, Count, Max
import uuid
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from Legajos.models import HistorialLegajoIndices, HistoricoIVI
from Legajos.forms import NuevoLegajoFamiliarForm
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied

# # Create your views here.
# derivaciones = LegajosDerivaciones.objects.filter(m2m_programas__nombr__iexact="CDIF")
# print(derivaciones)


def obtener_rol(request):
    if request.user.is_authenticated:
        # Supongamos que este método retorna los roles del usuario
        return list(request.user.groups.values_list("name", flat=True))
    return []


class CDIFDerivacionesBuscarListView(TemplateView, PermisosMixin):
    permission_required = "Usuarios.programa_CDIF"
    template_name = "SIF_CDIF/derivaciones_buscar.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        object_list = Legajos.objects.none()
        mostrar_resultados = False
        mostrar_btn_resetear = False
        query = self.request.GET.get("busqueda")

        if query:
            object_list = Legajos.objects.filter(
                Q(apellido__iexact=query) | Q(documento__iexact=query)
            ).distinct()
            if object_list and object_list.count() == 1:
                id = None
                for o in object_list:
                    pk = Legajos.objects.filter(id=o.id).first()
                return redirect("legajosderivaciones_historial", pk.id)

            if not object_list:
                messages.warning(self.request, ("La búsqueda no arrojó resultados."))

            rol = obtener_rol(self.request)
            roles_permitidos = [
                "CDIF  Administrador",
                "CDIF  Directivo",
                "CDIF  Equipo operativo",
                "CDIF  Equipo técnico",
                "CDIF  Consultante",
                # "CDIF  Observador",
            ]
            if self.request.user.is_superuser or any(
                role in roles_permitidos for role in rol
            ):
                context["btn_agregar"] = True
            else:
                context["btn_agregar"] = False

            mostrar_btn_resetear = True
            mostrar_resultados = True

        context["mostrar_resultados"] = mostrar_resultados
        context["mostrar_btn_resetear"] = mostrar_btn_resetear
        context["object_list"] = object_list
        return self.render_to_response(context)


class CDIFDerivacionesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.programa_CDIF"
    template_name = "SIF_CDIF/derivaciones_bandeja_list.html"
    queryset = LegajosDerivaciones.objects.filter(fk_programa=settings.PROG_CDIF)

    def get_context_data(self, **kwargs):
        context = super(CDIFDerivacionesListView, self).get_context_data(**kwargs)

        model = self.queryset

        query = self.request.GET.get("busqueda")

        if query:
            object_list = LegajosDerivaciones.objects.filter(
                (
                    Q(fk_legajo__apellido__iexact=query)
                    | Q(fk_legajo__nombre__iexact=query)
                )
                & Q(fk_programa=settings.PROG_CDIF)
            ).distinct()
            context["object_list"] = object_list
            model = object_list
            if not object_list:
                messages.warning(self.request, ("La búsqueda no arrojó resultados."))

        rol = obtener_rol(self.request)
        roles_permitidos = [
            "CDIF  Administrador",
            "CDIF  Directivo",
            "CDIF  Equipo operativo",
            "CDIF  Equipo técnico",
            # "CDIF  Consultante",
            # "CDIF  Observador",
        ]
        if self.request.user.is_superuser or any(
            role in roles_permitidos for role in rol
        ):
            context["btn_derivar"] = True
        else:
            context["btn_derivar"] = False

        context["todas"] = model
        context["pendientes"] = model.filter(estado="Pendiente")
        context["aceptadas"] = model.filter(estado="Aceptada")
        context["rechazadas"] = model.filter(estado="Rechazada")
        context["enviadas"] = model.filter(fk_usuario=self.request.user)
        return context


class CDIFDerivacionesDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_CDIF"
    template_name = "SIF_CDIF/derivaciones_detail.html"
    model = LegajosDerivaciones

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(
            pk=pk, fk_programa=settings.PROG_CDIF
        ).first()
        ivi = CDIF_IndiceIVI.objects.filter(fk_legajo_id=legajo.fk_legajo_id)
        resultado = (
            ivi.values("clave", "creado", "programa")
            .annotate(total=Sum("fk_criterios_ivi__puntaje"))
            .order_by("-creado")
        )

        rol = obtener_rol(self.request)
        roles_permitidos = [
            "CDIF  Administrador",
            "CDIF  Directivo",
            "CDIF  Equipo operativo",
            "CDIF  Equipo técnico",
            # "CDIF  Consultante",
            # "CDIF  Observador",
        ]
        if self.request.user.is_superuser or any(
            role in roles_permitidos for role in rol
        ):
            context["btn_aceptar"] = True
        else:
            context["btn_aceptar"] = False

        roles_permitidos_rechazar = [
            "CDIF  Administrador",
            "CDIF  Directivo",
            "CDIF  Equipo operativo",
            "CDIF  Equipo técnico",
            # "CDIF  Consultante",
            # "CDIF  Observador",
        ]
        if self.request.user.is_superuser or any(
            role in roles_permitidos_rechazar for role in rol
        ):
            context["btn_rechazar"] = True
        else:
            context["btn_rechazar"] = False

        roles_permitidos_eliminar_editar = [
            "CDIF  Administrador",
            # "CDIF  Directivo",
            # "CDIF  Equipo operativo",
            # "CDIF  Equipo técnico",
            # "CDIF  Consultante",
            # "CDIF  Observador",
        ]
        if self.request.user.is_superuser or any(
            role in roles_permitidos_eliminar_editar for role in rol
        ):
            context["btn_eliminar_editar"] = True
        else:
            context["btn_eliminar_editar"] = False

        context["pk"] = pk
        context["ivi"] = ivi
        context["resultado"] = resultado
        context["archivos"] = LegajosDerivacionesArchivos.objects.filter(
            legajo_derivacion=pk
        )
        return context


class CDIFDerivacionesRechazo(PermisosMixin, CreateView):
    permission_required = "Usuarios.programa_CDIF"
    template_name = "SIF_CDIF/derivaciones_rechazo.html"
    form_class = DerivacionesRechazoForm

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "CDIF  Administrador",
            "CDIF  Directivo",
            # "CDIF  Equipo operativo",
            "CDIF  Equipo técnico",
            # "CDIF  Consultante",
            # "CDIF  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa Administración
        grupos_usuario = request.user.groups.filter(name__startswith="CDIF")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(
            pk=pk, fk_programa=settings.PROG_CDIF
        ).first()
        context["object"] = legajo
        return context

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        base = LegajosDerivaciones.objects.get(pk=pk)
        base.motivo_rechazo = form.cleaned_data["motivo_rechazo"]
        base.obs_rechazo = form.cleaned_data["obs_rechazo"]
        base.estado = "Rechazada"
        base.fecha_rechazo = date.today()
        base.save()
        return HttpResponseRedirect(reverse("CDIF_derivaciones_listar"))

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("CDIF_derivaciones_listar")


class CDIFDerivacionesUpdateView(PermisosMixin, UpdateView):
    permission_required = "Usuarios.programa_CDIF"
    model = LegajosDerivaciones
    template_name = "SIF_CDIF/derivaciones_form.html"
    form_class = LegajosDerivacionesForm
    success_message = "Derivación editada con éxito"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "CDIF  Administrador",
            # "CDIF  Directivo",
            # "CDIF  Equipo operativo",
            # "CDIF  Equipo técnico",
            # "CDIF  Consultante",
            # "CDIF  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa Administración
        grupos_usuario = request.user.groups.filter(name__startswith="CDIF")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def get_initial(self):
        initial = super().get_initial()
        initial["fk_usuario"] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(id=pk).first()
        context["legajo"] = Legajos.objects.filter(id=legajo.fk_legajo.id).first()
        context["archivos_existentes"] = LegajosDerivacionesArchivos.objects.filter(
            legajo_derivacion=self.object
        )
        return context

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        delete_files = self.request.POST.getlist("delete_files")

        if delete_files:
            archivos = LegajosDerivacionesArchivos.objects.filter(id__in=delete_files)
            archivos.delete()

        return response

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("CDIF_derivaciones_ver", kwargs={"pk": pk})


class CDIFPreAdmisionesCreateView(PermisosMixin, CreateView, SuccessMessageMixin):
    permission_required = "Usuarios.programa_CDIF"
    template_name = "SIF_CDIF/preadmisiones_form.html"
    model = CDIF_PreAdmision
    form_class = CDIF_PreadmisionesForm
    form_nuevo_grupo_familiar_class = NuevoLegajoFamiliarForm()
    success_message = "Preadmisión creada correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "CDIF  Administrador",
            "CDIF  Directivo",
            "CDIF  Equipo operativo",
            "CDIF  Equipo técnico",
            # "CDIF  Consultante",
            # "CDIF  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa Administración
        grupos_usuario = request.user.groups.filter(name__startswith="CDIF")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        if "conviven" in self.request.POST:
            self.crear_grupo_hogar(self.request.POST)
            messages.success(self.request, "Familiar agregado correctamente.")
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(pk=pk).first()
        familia = LegajoGrupoFamiliar.objects.filter(fk_legajo_2_id=legajo.fk_legajo_id)
        # educacion = DimensionEducacion.objects.filter(fk_legajo=legajo.fk_legajo_id).first()
        familia_inversa = LegajoGrupoFamiliar.objects.filter(
            fk_legajo_1_id=legajo.fk_legajo_id
        )
        centros = Vacantes.objects.filter(fk_programa_id=settings.PROG_CDIF)
        cupos = CupoVacante.objects.filter(
            fk_vacante__fk_programa_id=settings.PROG_CDIF
        )
        context["pk"] = pk
        context["legajo"] = legajo
        context["familia"] = familia
        context["familia_inversa"] = familia_inversa
        context["centros"] = centros
        context["nuevo_grupo_familiar_form"] = self.form_nuevo_grupo_familiar_class
        context["cupos"] = cupos
        # context["educacion"] = educacion
        return context

    def crear_grupo_hogar(self, form: QueryDict):
        copy_form = dict(**form.dict())
        del copy_form["csrfmiddlewaretoken"]
        legajo_derivacion = LegajosDerivaciones.objects.filter(
            pk=copy_form.get("pk")
        ).first()
        vinculo = copy_form.get("vinculo")
        conviven = copy_form.get("conviven")
        estado_relacion = copy_form.get("estado_relacion")
        cuidador_principal = copy_form.get("cuidador_principal")
        max_nivel_send = copy_form.get("max_nivel")
        estado_nivel_send = copy_form.get("estado_nivel")

        # Crea el objeto Legajos
        try:

            nuevo_legajo = Legajos.objects.create(
                nombre=copy_form.get("nombre"),
                apellido=copy_form.get("apellido"),
                fecha_nacimiento=copy_form.get("fecha_nacimiento"),
                tipo_doc=copy_form.get("tipo_doc"),
                documento=copy_form.get("documento"),
                sexo=copy_form.get("sexo"),
            )

            DimensionFamilia.objects.create(fk_legajo=nuevo_legajo)
            DimensionVivienda.objects.create(fk_legajo=nuevo_legajo)
            DimensionSalud.objects.create(fk_legajo=nuevo_legajo)
            DimensionEconomia.objects.create(fk_legajo=nuevo_legajo)
            DimensionEducacion.objects.create(
                fk_legajo=nuevo_legajo,
                max_nivel=max_nivel_send,
                estado_nivel=estado_nivel_send,
            )
            DimensionTrabajo.objects.create(fk_legajo=nuevo_legajo)
        except Exception as e:
            print(e)
            return messages.error(
                self.request, "Verifique que no exista un legajo con ese DNI y NÚMERO."
            )

        # Crea el objeto LegajoGrupoFamiliar con los valores del formulario
        vinculo_data = VINCULO_MAP.get(vinculo)
        if not vinculo_data:
            return messages.error(self.request, "Vinculo inválido.")

        # crea la relacion de grupo familiar
        legajo_principal = legajo_derivacion.fk_legajo
        try:
            legajo_grupo_familiar = LegajoGrupoFamiliar.objects.create(
                fk_legajo_1=legajo_principal,
                fk_legajo_2=nuevo_legajo,
                vinculo=vinculo_data["vinculo"],
                vinculo_inverso=vinculo_data["vinculo_inverso"],
                conviven=conviven,
                estado_relacion=estado_relacion,
                cuidador_principal=cuidador_principal,
            )

            familiar = {
                "id": legajo_grupo_familiar.id,
                "fk_legajo_1": legajo_grupo_familiar.fk_legajo_1.id,
                "fk_legajo_2": legajo_grupo_familiar.fk_legajo_2.id,
                "vinculo": legajo_grupo_familiar.vinculo,
                "nombre": legajo_grupo_familiar.fk_legajo_2.nombre,
                "apellido": legajo_grupo_familiar.fk_legajo_2.apellido,
                "foto": (
                    legajo_grupo_familiar.fk_legajo_2.foto.url
                    if legajo_grupo_familiar.fk_legajo_2.foto
                    else None
                ),
                "cuidador_principal": legajo_grupo_familiar.cuidador_principal,
            }
        except Exception as e:
            print(e)
            return messages.error(
                self.request, "Verifique que no exista un legajo con ese DNI y NÚMERO."
            )

        # Redireccionar a la misma página después de realizar la acción con éxito
        # return HttpResponseRedirect(reverse('CDIF_preadmisiones_editar', args=[self.object.pk]))

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        form.instance.estado = "Pendiente"
        form.instance.vinculo1 = form.cleaned_data["vinculo1"]
        form.instance.vinculo2 = form.cleaned_data["vinculo2"]
        form.instance.vinculo3 = form.cleaned_data["vinculo3"]
        form.instance.vinculo4 = form.cleaned_data["vinculo4"]
        form.instance.vinculo5 = form.cleaned_data["vinculo5"]
        form.instance.creado_por_id = self.request.user.id

        self.object = form.save()

        base = LegajosDerivaciones.objects.get(pk=pk)
        base.estado = "Aceptada"
        base.save()

        # ---- Historial--------------
        legajo = LegajosDerivaciones.objects.filter(pk=pk).first()
        base = CDIF_Historial()
        base.fk_legajo_id = legajo.fk_legajo.id
        base.fk_legajo_derivacion_id = pk
        base.fk_preadmi_id = self.object.id
        base.movimiento = "ACEPTADO A PREADMISION"
        base.creado_por_id = self.request.user.id
        base.save()

        return HttpResponseRedirect(
            reverse("CDIF_preadmisiones_ver", args=[self.object.pk])
        )

    def form_invalid(self, form):
        return super().form_invalid(form)


class CDIFajaxLegajoDimensionEducacionView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_CDIF"
    model = DimensionEducacion

    def post(self, request, *args, **kwargs):
        if request.POST:
            datosDelFklegajoGuarda = DimensionEducacion.objects.filter(
                fk_legajo=request.POST.get("id")
            ).first()
            datosDelFklegajoGuarda_dict = model_to_dict(datosDelFklegajoGuarda)

        return JsonResponse(datosDelFklegajoGuarda_dict)


class CDIFajaxLegajoDimensionTrabajoView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_CDIF"
    model = DimensionTrabajo

    def post(self, request, *args, **kwargs):
        if request.POST:
            datosDelFklegajoGuarda = DimensionTrabajo.objects.filter(
                fk_legajo=request.POST.get("id")
            ).first()
            datosDelFklegajoGuarda_dict = model_to_dict(datosDelFklegajoGuarda)

        return JsonResponse(datosDelFklegajoGuarda_dict)


class CDIFPreAdmisionesUpdateView(PermisosMixin, UpdateView, SuccessMessageMixin):
    permission_required = "Usuarios.programa_CDIF"
    template_name = "SIF_CDIF/preadmisiones_form.html"
    model = CDIF_PreAdmision
    form_class = CDIF_PreadmisionesForm
    success_message = "Preadmisión creada correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "CDIF  Administrador",
            "CDIF  Directivo",
            "CDIF  Equipo operativo",
            "CDIF  Equipo técnico",
            # "CDIF  Consultante",
            # "CDIF  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa Administración
        grupos_usuario = request.user.groups.filter(name__startswith="CDIF")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        if "conviven" in self.request.POST:
            self.crear_grupo_hogar(self.request.POST)
            messages.success(self.request, "Familiar agregado correctamente.")
        pk = CDIF_PreAdmision.objects.filter(pk=self.kwargs["pk"]).first()
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(pk=pk.fk_derivacion_id).first()
        familia = LegajoGrupoFamiliar.objects.filter(fk_legajo_2_id=legajo.fk_legajo_id)
        familia_inversa = LegajoGrupoFamiliar.objects.filter(
            fk_legajo_1_id=legajo.fk_legajo_id
        )
        centros = Vacantes.objects.filter(fk_programa_id=settings.PROG_CDIF)
        cupos = CupoVacante.objects.filter(
            fk_vacante__fk_programa_id=settings.PROG_CDIF
        )

        if legajo.fk_legajo_id != None:
            datosDelFklegajoGuarda = DimensionEducacion.objects.get(
                fk_legajo=legajo.fk_legajo_id
            )
            datosDelFklegajoGuardaTrabajo = DimensionTrabajo.objects.get(
                fk_legajo=legajo.fk_legajo_id
            )

        context["pk"] = pk.fk_derivacion_id
        context["legajo"] = legajo
        context["familia"] = familia
        context["familia_inversa"] = familia_inversa
        context["centros"] = centros
        context["cupos"] = cupos
        context["nuevo_grupo_familiar_form"] = NuevoLegajoFamiliarForm()
        context["dimension_educacion_datos"] = datosDelFklegajoGuarda
        context["dimension_trabajo_datos"] = datosDelFklegajoGuardaTrabajo
        return context

    def crear_grupo_hogar(self, form: QueryDict):
        copy_form = dict(**form.dict())
        del copy_form["csrfmiddlewaretoken"]
        legajo_derivacion = LegajosDerivaciones.objects.filter(
            pk=copy_form.get("pk")
        ).first()
        vinculo = copy_form.get("vinculo")
        conviven = copy_form.get("conviven")
        estado_relacion = copy_form.get("estado_relacion")
        cuidador_principal = copy_form.get("cuidador_principal")

        # Crea el objeto Legajos
        try:

            nuevo_legajo = Legajos.objects.create(
                nombre=copy_form.get("nombre"),
                apellido=copy_form.get("apellido"),
                fecha_nacimiento=copy_form.get("fecha_nacimiento"),
                tipo_doc=copy_form.get("tipo_doc"),
                documento=copy_form.get("documento"),
                sexo=copy_form.get("sexo"),
            )

            print(nuevo_legajo)
            DimensionFamilia.objects.create(fk_legajo=nuevo_legajo)
            DimensionVivienda.objects.create(fk_legajo=nuevo_legajo)
            DimensionSalud.objects.create(fk_legajo=nuevo_legajo)
            DimensionEconomia.objects.create(fk_legajo=nuevo_legajo)
            DimensionEducacion.objects.create(fk_legajo=nuevo_legajo)
            DimensionTrabajo.objects.create(fk_legajo=nuevo_legajo)
        except Exception as e:
            print(e)
            return messages.error(
                self.request, "Verifique que no exista un legajo con ese DNI y NÚMERO."
            )

        # Crea el objeto LegajoGrupoFamiliar con los valores del formulario
        vinculo_data = VINCULO_MAP.get(vinculo)
        if not vinculo_data:
            return messages.error(self.request, "Vinculo inválido.")

        # crea la relacion de grupo familiar
        legajo_principal = legajo_derivacion.fk_legajo
        try:
            legajo_grupo_familiar = LegajoGrupoFamiliar.objects.create(
                fk_legajo_1=legajo_principal,
                fk_legajo_2=nuevo_legajo,
                vinculo=vinculo_data["vinculo"],
                vinculo_inverso=vinculo_data["vinculo_inverso"],
                conviven=conviven,
                estado_relacion=estado_relacion,
                cuidador_principal=cuidador_principal,
            )

            familiar = {
                "id": legajo_grupo_familiar.id,
                "fk_legajo_1": legajo_grupo_familiar.fk_legajo_1.id,
                "fk_legajo_2": legajo_grupo_familiar.fk_legajo_2.id,
                "vinculo": legajo_grupo_familiar.vinculo,
                "nombre": legajo_grupo_familiar.fk_legajo_2.nombre,
                "apellido": legajo_grupo_familiar.fk_legajo_2.apellido,
                "foto": (
                    legajo_grupo_familiar.fk_legajo_2.foto.url
                    if legajo_grupo_familiar.fk_legajo_2.foto
                    else None
                ),
                "cuidador_principal": legajo_grupo_familiar.cuidador_principal,
            }
        except Exception as e:
            print(e)
            return messages.error(
                self.request, "Verifique que no exista un legajo con ese DNI y NÚMERO."
            )

        # Redireccionar a la misma página después de realizar la acción con éxito
        # return HttpResponseRedirect(reverse('CDLE_preadmisiones_editar', args=[self.object.pk]))

    def form_invalid(self, form):
        # Imprimir todos los errores del formulario
        print("Errores del formulario:", form.errors)

        # Iterar sobre los errores del formulario y registrar los campos inválidos
        for field, errors in form.errors.items():
            print(f"Campo inválido: {field}")
            for error in errors:
                print(f" - Error: {error}")

        return super().form_invalid(form)

    def form_valid(self, form):
        pk = CDIF_PreAdmision.objects.filter(pk=self.kwargs["pk"]).first()
        form.instance.creado_por_id = pk.creado_por_id
        form.instance.vinculo1 = form.cleaned_data["vinculo1"]
        form.instance.vinculo2 = form.cleaned_data["vinculo2"]
        form.instance.vinculo3 = form.cleaned_data["vinculo3"]
        form.instance.vinculo4 = form.cleaned_data["vinculo4"]
        form.instance.vinculo5 = form.cleaned_data["vinculo5"]
        form.instance.estado = pk.estado
        form.instance.modificado_por_id = self.request.user.id
        sala = form.cleaned_data["sala_postula"]
        self.object = form.save()

        return HttpResponseRedirect(
            reverse("CDIF_preadmisiones_ver", args=[self.object.pk])
        )


class CDIFPreAdmisionesDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_CDIF"
    template_name = "SIF_CDIF/preadmisiones_detail.html"
    model = CDIF_PreAdmision

    def get_context_data(self, **kwargs):
        pk = CDIF_PreAdmision.objects.filter(pk=self.kwargs["pk"]).first()
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(pk=pk.fk_derivacion_id).first()
        familia = LegajoGrupoFamiliar.objects.filter(fk_legajo_2_id=legajo.fk_legajo_id)
        ivi = CDIF_IndiceIVI.objects.filter(fk_legajo_id=legajo.fk_legajo_id)
        resultado = (
            ivi.values("clave", "creado", "programa")
            .annotate(total=Sum("fk_criterios_ivi__puntaje"))
            .order_by("-creado")
        )

        rol = obtener_rol(self.request)
        roles_permitidos = [
            "CDIF  Administrador",
            "CDIF  Directivo",
            "CDIF  Equipo operativo",
            "CDIF  Equipo técnico",
            # "CDIF  Consultante",
            # "CDIF  Observador",
        ]
        if self.request.user.is_superuser or any(
            role in roles_permitidos for role in rol
        ):
            context["btn_admitir"] = True
        else:
            context["btn_admitir"] = False

        roles_rechazo = [
            "CDIF  Administrador",
            "CDIF  Directivo",
            # "CDIF  Equipo operativo",
            "CDIF  Equipo técnico",
            # "CDIF  Consultante",
            # "CDIF  Observador",
        ]
        if self.request.user.is_superuser or any(role in roles_rechazo for role in rol):
            context["btn_rechazar"] = True
        else:
            context["btn_rechazar"] = False

        context["ivi"] = ivi
        context["resultado"] = resultado
        context["legajo"] = legajo
        context["familia"] = familia

        criterio = CDIF_IndiceIVI.objects.filter(fk_preadmi_id=pk, tipo="Ingreso")
        foto_ivi = CDIF_Foto_IVI.objects.filter(
            fk_preadmi_id=pk, tipo="Ingreso"
        ).first()
        if criterio:
            context["criterio"] = criterio
            context["puntaje"] = criterio.aggregate(
                total=Sum("fk_criterios_ivi__puntaje")
            )
            context["cantidad"] = criterio.count()
            context["modificables"] = criterio.filter(
                fk_criterios_ivi__modificable__icontains="Potencial"
            ).count()
            context["mod_puntaje"] = criterio.filter(
                fk_criterios_ivi__modificable__icontains="Potencial"
            ).aggregate(total=Sum("fk_criterios_ivi__puntaje"))
            context["ajustes"] = criterio.filter(
                fk_criterios_ivi__tipo="Ajustes"
            ).count()
        if foto_ivi:
            context["foto_ivi"] = foto_ivi
            context["maximo"] = foto_ivi.puntaje_max
        return context

    def post(self, request, *args, **kwargs):
        if "admitir" in request.POST:
            preadmi = CDIF_PreAdmision.objects.filter(pk=self.kwargs["pk"]).first()
            preadmi.admitido = "SI"
            preadmi.save()

            base1 = CDIF_Admision()
            base1.fk_preadmi_id = preadmi.pk
            base1.creado_por_id = self.request.user.id
            base1.save()
            redirigir = base1.pk

            # ---------HISTORIAL---------------------------------
            pk = self.kwargs["pk"]
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
            return redirect("CDIF_asignado_admisiones_ver", redirigir)
        if "finalizar_preadm" in request.POST:
            # Realiza la actualización del campo aquí
            objeto = self.get_object()
            objeto.estado = "Pendiente"
            objeto.ivi = "Pendiente"
            objeto.admitido = "NO"
            objeto.save()

            # ---------HISTORIAL---------------------------------
            pk = self.kwargs["pk"]
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

        if "listaespera" in request.POST:
            # Realiza la actualización del campo aquí
            objeto = self.get_object()
            objeto.estado = "Lista de espera"
            objeto.save()

            # ---------HISTORIAL---------------------------------
            pk = self.kwargs["pk"]
            legajo = CDIF_PreAdmision.objects.filter(pk=pk).first()
            base = CDIF_Historial()
            base.fk_legajo_id = legajo.fk_legajo.id
            base.fk_legajo_derivacion_id = legajo.fk_derivacion_id
            base.fk_preadmi_id = pk
            base.movimiento = "LISTA DE ESPERA"
            base.creado_por_id = self.request.user.id
            base.save()
            # Redirige de nuevo a la vista de detalle actualizada
            return HttpResponseRedirect(self.request.path_info)

        if "rechazar" in request.POST:
            # Realiza la actualización del campo aquí
            objeto = self.get_object()
            objeto.estado = "Rechazado"
            objeto.save()

            # ---------HISTORIAL---------------------------------
            pk = self.kwargs["pk"]
            legajo = CDIF_PreAdmision.objects.filter(pk=pk).first()
            base = CDIF_Historial()
            base.fk_legajo_id = legajo.fk_legajo.id
            base.fk_legajo_derivacion_id = legajo.fk_derivacion_id
            base.fk_preadmi_id = pk
            base.movimiento = "Rechazado"
            base.creado_por_id = self.request.user.id
            base.save()
            # Redirige de nuevo a la vista de detalle actualizada
            return HttpResponseRedirect(self.request.path_info)


class CDIFPreAdmisionesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.programa_CDIF"
    template_name = "SIF_CDIF/preadmisiones_list.html"
    model = CDIF_PreAdmision

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "CDIF  Administrador",
            "CDIF  Directivo",
            "CDIF  Equipo operativo",
            "CDIF  Equipo técnico",
            "CDIF  Consultante",
            # "CDIF  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa Administración
        grupos_usuario = request.user.groups.filter(name__startswith="CDIF")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pre_admi = CDIF_PreAdmision.objects.all()
        context["object"] = pre_admi
        return context


class CDIFPreAdmisionesBuscarListView(PermisosMixin, TemplateView):
    permission_required = "Usuarios.programa_CDIF"
    template_name = "SIF_CDIF/preadmisiones_buscar.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        object_list = CDIF_PreAdmision.objects.none()
        mostrar_resultados = False
        mostrar_btn_resetear = False
        query = self.request.GET.get("busqueda")
        if query:
            object_list = (
                CDIF_PreAdmision.objects.filter(
                    Q(fk_legajo__apellido__iexact=query)
                    | Q(fk_legajo__documento__iexact=query),
                    fk_derivacion__fk_programa_id=settings.PROG_CDIF,
                )
                .exclude(estado__in=["Rechazada", "Aceptada"])
                .distinct()
            )
            # object_list = Legajos.objects.filter(Q(apellido__iexact=query) | Q(documento__iexact=query))
            if not object_list:
                messages.warning(self.request, ("La búsqueda no arrojó resultados."))

            mostrar_btn_resetear = True
            mostrar_resultados = True

        context["mostrar_resultados"] = mostrar_resultados
        context["mostrar_btn_resetear"] = mostrar_btn_resetear
        context["object_list"] = object_list

        return self.render_to_response(context)


class CDIFPreAdmisionesDeleteView(PermisosMixin, DeleteView):
    permission_required = "Usuarios.programa_CDIF"
    model = CDIF_PreAdmision
    template_name = "SIF_CDIF/preadmisiones_confirm_delete.html"
    success_url = reverse_lazy("CDIF_preadmisiones_listar")

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "CDIF  Administrador",
            # "CDIF  Directivo",
            # "CDIF  Equipo operativo",
            # "CDIF  Equipo técnico",
            # "CDIF  Consultante",
            # "CDIF  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa Administración
        grupos_usuario = request.user.groups.filter(name__startswith="CDIF")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def form_valid(self, form):
        if self.object.estado != "Pendiente":
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


class CDIFPreAdmisionesRechazarView(PermisosMixin, DeleteView):
    permission_required = "Usuarios.programa_CDIF"
    model = CDIF_PreAdmision
    template_name = "SIF_CDIF/preadmisiones_confirm_rechazar.html"
    success_url = reverse_lazy("CDIF_preadmisiones_listar")

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "CDIF  Administrador",
            "CDIF  Directivo",
            # "CDIF  Equipo operativo",
            "CDIF  Equipo técnico",
            # "CDIF  Consultante",
            # "CDIF  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa Administración
        grupos_usuario = request.user.groups.filter(name__startswith="CDIF")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def form_valid(self, form):
        if self.object.estado == "Rechazado":
            messages.error(
                self.request,
                "Esta solicitud ya ha sido rechazada.",
            )
            return redirect("CDIF_preadmisiones_ver", pk=int(self.object.id))
        else:
            self.object.estado = "Rechazado"
            self.object.observaciones = self.request.POST.get("observaciones")
            self.object.save()
        return redirect("CDIF_preadmisiones_ver", pk=int(self.object.id))


class CDIFCriteriosIVICreateView(PermisosMixin, CreateView):
    permission_required = "Usuarios.programa_CDIF"
    template_name = "SIF_CDIF/criterios_ivi_form.html"
    model = Criterios_IVI
    form_class = criterios_IVI

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse("CDIF_criterios_ivi_crear"))


class CDIFIndiceIviCreateView(PermisosMixin, CreateView):
    permission_required = "Usuarios.programa_CDIF"
    model = Criterios_IVI
    template_name = "SIF_CDIF/indiceivi_form.html"
    form_class = CDIF_IndiceIviForm

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "CDIF  Administrador",
            "CDIF  Directivo",
            "CDIF  Equipo operativo",
            "CDIF  Equipo técnico",
            # "CDIF  Consultante",
            # "CDIF  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa Administración
        grupos_usuario = request.user.groups.filter(name__startswith="CDIF")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        object = CDIF_PreAdmision.objects.filter(pk=pk).first()
        # object = Legajos.objects.filter(pk=pk).first()
        criterio = Criterios_IVI.objects.all()
        context["object"] = object
        context["criterio"] = criterio
        context["form2"] = CDIF_IndiceIviHistorialForm()
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        # Genera una clave única utilizando uuid4 (versión aleatoria)
        preadmi = CDIF_PreAdmision.objects.filter(pk=pk).first()
        clave = str(uuid.uuid4())
        nombres_campos = request.POST.keys()
        puntaje_maximo = Criterios_IVI.objects.aggregate(total=Sum("puntaje"))["total"]
        total_puntaje = 0
        historico = HistorialLegajoIndices()
        for f in nombres_campos:
            if f.isdigit():
                criterio_ivi = Criterios_IVI.objects.filter(id=f).first()
                # Sumar el valor de f al total_puntaje
                total_puntaje += int(criterio_ivi.puntaje)
                base = CDIF_IndiceIVI()
                base.fk_criterios_ivi_id = f
                base.fk_legajo_id = preadmi.fk_legajo_id
                base.fk_preadmi_id = pk
                base.tipo = "Ingreso"
                base.presencia = True
                base.programa = "CDIF"
                historico.programa = base.programa
                base.clave = clave
                base.save()
        # total_puntaje contiene la suma de los valores de F
        foto = CDIF_Foto_IVI()
        foto.observaciones = request.POST.get("observaciones", "")
        foto.fk_preadmi_id = pk
        foto.fk_legajo_id = preadmi.fk_legajo_id
        foto.puntaje = total_puntaje
        foto.puntaje_max = puntaje_maximo
        # foto.crit_modificables = crit_modificables
        # foto.crit_presentes = crit_presentes
        foto.tipo = "Ingreso"
        foto.clave = clave
        foto.creado_por_id = self.request.user.id

        historico.observaciones = foto.observaciones
        historico.fk_legajo_id = preadmi.fk_legajo_id
        historico.puntaje = total_puntaje
        historico.puntaje_total = total_puntaje
        historico.puntaje_max = puntaje_maximo
        historico.tipo = "Ingreso"
        historico.clave = clave

        historico.save()
        foto.save()

        preadmi.ivi = "SI"
        preadmi.save()

        # ---------HISTORIAL---------------------------------
        pk = self.kwargs["pk"]
        base = CDIF_Historial()
        base.fk_legajo_id = preadmi.fk_legajo.id
        base.fk_legajo_derivacion_id = preadmi.fk_derivacion_id
        base.fk_preadmi_id = preadmi.id
        base.movimiento = "CREACION IVI"
        base.creado_por_id = self.request.user.id
        base.save()

        return redirect("CDIF_indiceivi_ver", preadmi.id)


class CDIFIndiceIviUpdateView(PermisosMixin, UpdateView):
    permission_required = "Usuarios.programa_CDIF"
    template_name = "SIF_CDIF/indiceivi_edit.html"
    model = CDIF_PreAdmision
    form_class = CDIF_IndiceIviForm

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "CDIF  Administrador",
            # "CDIF  Directivo",
            "CDIF  Equipo operativo",
            "CDIF  Equipo técnico",
            # "CDIF  Consultante",
            # "CDIF  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa Administración
        grupos_usuario = request.user.groups.filter(name__startswith="CDIF")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        activos = CDIF_IndiceIVI.objects.filter(fk_preadmi_id=pk)
        observaciones = CDIF_Foto_IVI.objects.filter(fk_preadmi_id=pk).first()

        context = super().get_context_data(**kwargs)
        context["object"] = CDIF_PreAdmision.objects.filter(pk=pk).first()
        context["activos"] = activos
        context["clave"] = observaciones.clave
        context["observaciones"] = observaciones.observaciones
        context["criterio"] = Criterios_IVI.objects.all()
        context["form2"] = CDIF_IndiceIviHistorialForm()
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        preadmi = CDIF_PreAdmision.objects.filter(pk=pk).first()
        cdif_foto = CDIF_Foto_IVI.objects.filter(fk_preadmi_id=pk).first()
        clave = cdif_foto.clave
        indices_ivi = CDIF_IndiceIVI.objects.filter(clave=clave)
        # cdif_foto.delete()
        indices_ivi.delete()
        nombres_campos = request.POST.keys()
        puntaje_maximo = Criterios_IVI.objects.aggregate(total=Sum("puntaje"))["total"]
        total_puntaje = 0
        for f in nombres_campos:
            if f.isdigit():
                criterio_ivi = Criterios_IVI.objects.filter(id=f).first()
                # Sumar el valor de f al total_puntaje
                total_puntaje += int(criterio_ivi.puntaje)
                base = CDIF_IndiceIVI()
                base.fk_criterios_ivi_id = f
                base.fk_legajo_id = preadmi.fk_legajo_id
                base.fk_preadmi_id = pk
                base.presencia = True
                base.programa = "CDIF"
                base.tipo = "Ingreso"
                base.clave = clave
                base.save()

        # total_puntaje contiene la suma de los valores de F
        foto = CDIF_Foto_IVI.objects.filter(clave=clave).first()
        foto.observaciones = request.POST.get("observaciones", "")
        foto.fk_preadmi_id = pk
        foto.fk_legajo_id = preadmi.fk_legajo_id
        foto.puntaje = total_puntaje
        foto.puntaje_max = puntaje_maximo
        # foto.crit_modificables = crit_modificables
        # foto.crit_presentes = crit_presentes
        foto.tipo = "Ingreso"
        foto.clave = clave
        foto.modificado_por_id = self.request.user.id
        foto.save()

        # ---------HISTORIAL---------------------------------
        pk = self.kwargs["pk"]
        preadmi = CDIF_PreAdmision.objects.filter(pk=pk).first()
        base = CDIF_Historial()
        base.fk_legajo_id = preadmi.fk_legajo.id
        base.fk_legajo_derivacion_id = preadmi.fk_derivacion_id
        base.fk_preadmi_id = preadmi.id
        base.movimiento = "MODIFICACION IVI"
        base.creado_por_id = self.request.user.id
        base.save()

        return redirect("CDIF_indiceivi_ver", preadmi.id)


class CDIFIndiceIviDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_CDIF"
    template_name = "SIF_CDIF/indiceivi_detail.html"
    model = CDIF_PreAdmision

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        criterio = CDIF_IndiceIVI.objects.filter(fk_preadmi_id=pk, tipo="Ingreso")
        object = CDIF_PreAdmision.objects.filter(pk=pk).first()
        foto_ivi = CDIF_Foto_IVI.objects.filter(
            fk_preadmi_id=pk, tipo="Ingreso"
        ).first()

        context["object"] = object
        context["foto_ivi"] = foto_ivi
        context["criterio"] = criterio
        context["puntaje"] = criterio.aggregate(total=Sum("fk_criterios_ivi__puntaje"))
        context["cantidad"] = criterio.count()
        context["modificables"] = criterio.filter(
            fk_criterios_ivi__modificable__icontains="Potencial"
        ).count()
        context["mod_puntaje"] = criterio.filter(
            fk_criterios_ivi__modificable__icontains="Potencial"
        ).aggregate(total=Sum("fk_criterios_ivi__puntaje"))
        context["ajustes"] = criterio.filter(fk_criterios_ivi__tipo="Ajustes").count()
        # context['maximo'] = foto_ivi.puntaje_max
        return context


class CDIFPreAdmisiones2DetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_CDIF"
    template_name = "SIF_CDIF/preadmisiones_detail2.html"
    model = CDIF_PreAdmision


class CDIFPreAdmisiones3DetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_CDIF"
    template_name = "SIF_CDIF/preadmisiones_detail3.html"
    model = CDIF_PreAdmision

    def get_context_data(self, **kwargs):
        pk = CDIF_PreAdmision.objects.filter(pk=self.kwargs["pk"]).first()
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(pk=pk.fk_derivacion_id).first()
        familia = LegajoGrupoFamiliar.objects.filter(fk_legajo_2_id=legajo.fk_legajo_id)
        criterio = CDIF_IndiceIVI.objects.filter(fk_preadmi_id=pk, tipo="Ingreso")
        foto_ivi = CDIF_Foto_IVI.objects.filter(
            fk_preadmi_id=pk, tipo="Ingreso"
        ).first()

        context["legajo"] = legajo
        context["familia"] = familia
        context["foto_ivi"] = foto_ivi
        context["puntaje"] = foto_ivi.puntaje
        context["cantidad"] = criterio.count()
        context["modificables"] = criterio.filter(
            fk_criterios_ivi__modificable__icontains="Potencial"
        ).count()
        context["mod_puntaje"] = criterio.filter(
            fk_criterios_ivi__modificable__icontains="Potencial"
        ).aggregate(total=Sum("fk_criterios_ivi__puntaje"))
        context["ajustes"] = criterio.filter(fk_criterios_ivi__tipo="Ajustes").count()
        context["maximo"] = foto_ivi.puntaje_max
        return context

    def post(self, request, *args, **kwargs):
        if "admitir" in request.POST:
            preadmi = CDIF_PreAdmision.objects.filter(pk=self.kwargs["pk"]).first()
            preadmi.admitido = "SI"
            preadmi.estado = "Admitido"
            preadmi.save()

            base1 = CDIF_Admision()
            base1.fk_preadmi_id = preadmi.pk
            base1.estado_vacante = "Lista de espera"
            base1.creado_por_id = self.request.user.id
            base1.save()
            redirigir = base1.pk

            # ---------HISTORIAL---------------------------------
            pk = self.kwargs["pk"]
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
            return redirect("CDIF_admisiones_ver", redirigir)


class CDIFAdmisionesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.programa_CDIF"
    template_name = "SIF_CDIF/adminsiones_list.html"
    model = CDIF_Admision

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "CDIF  Administrador",
            "CDIF  Directivo",
            "CDIF  Equipo operativo",
            "CDIF  Equipo técnico",
            "CDIF  Consultante",
            # "CDIF  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa Administración
        grupos_usuario = request.user.groups.filter(name__startswith="CDIF")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        criterio = CDIF_IndiceIVI.objects.all()
        admi = CDIF_Admision.objects.all()
        foto = CDIF_Foto_IVI.objects.all()

        context["admi"] = admi
        context["foto"] = foto
        context["puntaje"] = criterio.aggregate(total=Sum("fk_criterios_ivi__puntaje"))
        return context


class CDIFAdmisionesDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_CDIF"
    model = CDIF_Admision
    template_name = "SIF_CDIF/admisiones_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = CDIF_Admision.objects.filter(pk=self.kwargs["pk"]).first()
        preadmi = CDIF_PreAdmision.objects.filter(pk=pk.fk_preadmi_id).first()
        criterio = CDIF_IndiceIVI.objects.filter(fk_preadmi_id=preadmi, tipo="Ingreso")
        foto_ivi = CDIF_Foto_IVI.objects.filter(
            fk_preadmi_id=preadmi, tipo="Ingreso"
        ).first()

        context["foto_ivi"] = foto_ivi
        context["puntaje"] = foto_ivi.puntaje
        context["cantidad"] = criterio.count()
        context["modificables"] = criterio.filter(
            fk_criterios_ivi__modificable__icontains="Potencial"
        ).count()
        context["mod_puntaje"] = criterio.filter(
            fk_criterios_ivi__modificable__icontains="Potencial"
        ).aggregate(total=Sum("fk_criterios_ivi__puntaje"))
        context["ajustes"] = criterio.filter(fk_criterios_ivi__tipo="Ajustes").count()
        context["maximo"] = foto_ivi.puntaje_max

        return context


class CDIFVacantesAdmision(PermisosMixin, CreateView):
    permission_required = "Usuarios.programa_CDIF"
    model = CDIF_Admision
    template_name = "SIF_CDIF/vacantes_form.html"
    form_class = CDIF_VacantesOtorgadasForm

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "CDIF  Administrador",
            "CDIF  Directivo",
            "CDIF  Equipo operativo",
            "CDIF  Equipo técnico",
            # "CDIF  Consultante",
            # "CDIF  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa Administración
        grupos_usuario = request.user.groups.filter(name__startswith="CDIF")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def form_valid(self, form):
        self.object = form.save()

        base1 = CDIF_Admision.objects.filter(pk=self.kwargs["pk"]).first()
        base1.estado_vacante = "Asignada"
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

        return redirect("CDIF_asignado_admisiones_ver", legajo.pk)

    def form_invalid(self, form):
        errors = form.errors
        print(errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = CDIF_Admision.objects.filter(pk=self.kwargs["pk"]).first()

        preadmi = CDIF_PreAdmision.objects.filter(pk=pk.fk_preadmi_id).first()
        criterio = CDIF_IndiceIVI.objects.filter(fk_preadmi_id=preadmi, tipo="Ingreso")
        foto_ivi = CDIF_Foto_IVI.objects.filter(
            fk_preadmi_id=preadmi, tipo="Ingreso"
        ).first()
        centros = Vacantes.objects.filter(fk_programa_id=settings.PROG_CDIF)
        cupos = CupoVacante.objects.filter(
            fk_vacante__fk_programa_id=settings.PROG_CDIF
        )

        context["object"] = pk
        context["foto_ivi"] = foto_ivi
        context["puntaje"] = foto_ivi.puntaje
        context["cantidad"] = criterio.count()
        context["modificables"] = criterio.filter(
            fk_criterios_ivi__modificable__icontains="Potencialsi"
        ).count()
        context["mod_puntaje"] = criterio.filter(
            fk_criterios_ivi__modificable__icontains="Potencial"
        ).aggregate(total=Sum("fk_criterios_ivi__puntaje"))
        context["ajustes"] = criterio.filter(fk_criterios_ivi__tipo="Ajustes").count()
        context["maximo"] = foto_ivi.puntaje_max
        context["centros"] = centros
        context["cupos"] = cupos

        return context


class CDIFVacantesAdmisionCambio(PermisosMixin, CreateView):
    permission_required = "Usuarios.programa_CDIF"
    model = CDIF_Admision
    template_name = "SIF_CDIF/vacantes_form_cambio.html"
    form_class = CDIF_VacantesOtorgadasForm

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "CDIF  Administrador",
            # "CDIF  Directivo",
            "CDIF  Equipo operativo",
            # "CDIF  Equipo técnico",
            # "CDIF  Consultante",
            # "CDIF  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa Administración
        grupos_usuario = request.user.groups.filter(name__startswith="CDIF")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def form_valid(self, form):
        # if form.cleaned_data['fecha_egreso'] == None:
        #     messages.error(self.request, 'El campo fecha de egreso es requerido.')
        #     return super().form_invalid(form)
        # else:
        form.evento = "CambioVacante"
        pk = self.kwargs["pk"]
        vacante_anterior = CDIF_VacantesOtorgadas.objects.filter(
            fk_admision_id=pk
        ).last()
        vacante_anterior.estado_vacante = "Cambiado"
        vacante_anterior.motivo = form.cleaned_data["motivo"]
        vacante_anterior.fecha_egreso = date.today()
        vacante_anterior.save()

        form.cleaned_data["motivo"] = ""
        self.object = form.save()

        # --------- HISTORIAL ---------------------------------

        legajo = CDIF_Admision.objects.filter(pk=pk).first()
        base = CDIF_Historial()
        base.fk_legajo_id = legajo.fk_preadmi.fk_legajo.id
        base.fk_legajo_derivacion_id = legajo.fk_preadmi.fk_derivacion_id
        base.fk_preadmi_id = legajo.fk_preadmi.pk
        base.fk_admision_id = pk
        base.movimiento = "CAMBIO VACANTE"
        base.creado_por_id = self.request.user.id
        base.save()

        return redirect("CDIF_asignado_admisiones_ver", legajo.id)

    # def form_invalid(self, form):
    #    errors = form.errors
    #    print(errors)
    #    return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = CDIF_Admision.objects.filter(pk=self.kwargs["pk"]).first()
        vacante_otorgada = CDIF_VacantesOtorgadas.objects.filter(
            fk_admision_id=self.kwargs["pk"]
        ).first()

        preadmi = CDIF_PreAdmision.objects.filter(pk=pk.fk_preadmi_id).first()
        criterio = CDIF_IndiceIVI.objects.filter(fk_preadmi_id=preadmi, tipo="Ingreso")
        foto_ivi = CDIF_Foto_IVI.objects.filter(
            fk_preadmi_id=preadmi, tipo="Ingreso"
        ).first()
        centros = Vacantes.objects.filter(fk_programa_id=settings.PROG_CDIF)
        cupos = CupoVacante.objects.filter(
            fk_vacante__fk_programa_id=settings.PROG_CDIF
        )

        context["object"] = pk
        context["observaciones"] = foto_ivi
        context["puntaje"] = foto_ivi.puntaje
        context["cantidad"] = criterio.count()
        context["modificables"] = criterio.filter(
            fk_criterios_ivi__modificable__icontains="Potencial"
        ).count()
        context["mod_puntaje"] = criterio.filter(
            fk_criterios_ivi__modificable__icontains="Potencial"
        ).aggregate(total=Sum("fk_criterios_ivi__puntaje"))
        context["ajustes"] = criterio.filter(fk_criterios_ivi__tipo="Ajustes").count()
        context["maximo"] = foto_ivi.puntaje_max
        context["vo"] = vacante_otorgada
        context["centros"] = centros
        context["cupos"] = cupos

        return context


class CDIFAsignadoAdmisionDetail(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_CDIF"
    template_name = "SIF_CDIF/asignado_admisiones_detail.html"
    model = CDIF_Admision

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        admi = CDIF_Admision.objects.filter(pk=self.kwargs["pk"]).first()

        preadmi = CDIF_PreAdmision.objects.filter(pk=admi.fk_preadmi_id).first()
        criterio = CDIF_IndiceIVI.objects.filter(fk_preadmi_id=preadmi, tipo="Ingreso")
        criterio2 = CDIF_IndiceIVI.objects.filter(fk_preadmi_id=preadmi, tipo="Ingreso")
        observaciones = CDIF_Foto_IVI.objects.filter(
            fk_preadmi_id=preadmi, tipo="Ingreso"
        ).first()
        observaciones2 = CDIF_Foto_IVI.objects.filter(
            fk_preadmi_id=preadmi, tipo="Ingreso"
        ).first()
        lastVO = CDIF_VacantesOtorgadas.objects.filter(fk_admision_id=admi.id).last()
        movimientosVO = CDIF_VacantesOtorgadas.objects.filter(
            fk_admision_id=admi.id
        ).all()
        intervenciones = CDIF_Intervenciones.objects.filter(
            fk_admision_id=admi.id
        ).all()
        intervenciones_last = CDIF_Intervenciones.objects.filter(
            fk_admision_id=admi.id
        ).last()
        foto_ivi_fin = CDIF_Foto_IVI.objects.filter(
            fk_preadmi_id=admi.fk_preadmi_id, tipo="Ingreso"
        ).last()
        foto_ivi_inicio = CDIF_Foto_IVI.objects.filter(
            fk_preadmi_id=admi.fk_preadmi_id, tipo="Ingreso"
        ).first()

        rol = obtener_rol(self.request)
        roles_inactivar = [
            "CDIF  Administrador",
            "CDIF  Directivo",
            "CDIF  Equipo operativo",
            "CDIF  Equipo técnico",
            # "CDIF  Consultante",
            # "CDIF  Observador",
        ]
        if self.request.user.is_superuser or any(
            role in roles_inactivar for role in rol
        ):
            context["btn_inactivar"] = True
        else:
            context["btn_inactivar"] = False

        context["foto_ivi_fin"] = foto_ivi_fin
        context["foto_ivi_inicio"] = foto_ivi_inicio
        context["observaciones"] = observaciones
        context["observaciones2"] = observaciones2
        context["criterio"] = criterio
        context["puntaje"] = criterio.aggregate(total=Sum("fk_criterios_ivi__puntaje"))
        context["puntaje2"] = criterio2.aggregate(
            total=Sum("fk_criterios_ivi__puntaje")
        )
        context["object"] = admi
        context["vo"] = self.object
        context["lastvo"] = lastVO
        context["movimientosVO"] = movimientosVO
        context["intervenciones_count"] = intervenciones.count()
        context["intervenciones_last"] = intervenciones_last

        return context


class CDIFInactivaAdmisionDetail(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_CDIF"
    template_name = "SIF_CDIF/inactiva_admisiones_detail.html"
    model = CDIF_Admision

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        admi = CDIF_Admision.objects.filter(pk=self.kwargs["pk"]).first()

        preadmi = CDIF_PreAdmision.objects.filter(pk=admi.fk_preadmi_id).first()
        criterio = CDIF_IndiceIVI.objects.filter(fk_preadmi_id=preadmi, tipo="Egreso")
        lastVO = CDIF_VacantesOtorgadas.objects.filter(fk_admision_id=admi.id).last()
        movimientosVO = CDIF_VacantesOtorgadas.objects.filter(
            fk_admision_id=admi.id
        ).all()
        intervenciones = CDIF_Intervenciones.objects.filter(
            fk_admision_id=admi.id
        ).all()
        intervenciones_last = CDIF_Intervenciones.objects.filter(
            fk_admision_id=admi.id
        ).last()
        foto_ivi_fin = CDIF_Foto_IVI.objects.filter(
            fk_preadmi_id=admi.fk_preadmi_id, tipo="Egreso"
        ).first()
        foto_ivi_inicio = CDIF_Foto_IVI.objects.filter(
            fk_preadmi_id=admi.fk_preadmi_id, tipo="Ingreso"
        ).first()

        context["foto_ivi_fin"] = foto_ivi_fin
        context["foto_ivi_inicio"] = foto_ivi_inicio
        context["criterio"] = criterio
        context["object"] = admi
        context["vo"] = self.object
        context["lastvo"] = lastVO
        context["movimientosVO"] = movimientosVO
        context["intervenciones_count"] = intervenciones.count()
        context["intervenciones_last"] = intervenciones_last

        return context


class CDIFVacantesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.programa_CDIF"
    model = Vacantes
    template_name = "SIF_CDIF/vacantes_list.html"
    context_object_name = "organizaciones"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "CDIF  Administrador",
            "CDIF  Directivo",
            "CDIF  Equipo operativo",
            "CDIF  Equipo técnico",
            "CDIF  Consultante",
            # "CDIF  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa Administración
        grupos_usuario = request.user.groups.filter(name__startswith="CDIF")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        centros = Vacantes.objects.filter(fk_programa_id=settings.PROG_CDIF)
        cupos = CupoVacante.objects.filter(
            fk_vacante__fk_programa_id=settings.PROG_CDIF
        )
        asignada = CDIF_VacantesOtorgadas.objects.filter(estado_vacante="Asignada")

        # Crear una lista para almacenar los resultados con el conteo
        resultados = []
        for cupo in cupos:
            contador_aciertos = asignada.filter(sala_id=cupo.id).count()
            resultados.append({"cupo": cupo, "aciertos": contador_aciertos})

        context["centros"] = centros
        context["cupos"] = cupos
        context["asignada"] = asignada
        context["resultados"] = resultados

        return context


class CDIFVacantesDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_CDIF"
    template_name = "SIF_CDIF/vacantes_detail.html"
    model = Vacantes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        admi = CDIF_VacantesOtorgadas.objects.filter(
            fk_organismo_id=self.kwargs["pk"],
            fk_admision__estado="Activa",
            estado_vacante="Asignada",
        )
        admi2 = CDIF_Admision.objects.filter(
            fk_preadmi__centro_postula_id=self.kwargs["pk"],
            estado="Activa",
            estado_vacante="Lista de espera",
        )
        cupos = CupoVacante.objects.filter(fk_vacante_id=self.kwargs["pk"])
        asignada = CDIF_VacantesOtorgadas.objects.filter(
            fk_organismo_id=self.kwargs["pk"], estado_vacante="Asignada"
        )
        ivi = CDIF_Foto_IVI.objects.filter(tipo="Ingreso").all()

        # Crear una lista para almacenar los resultados con el conteo
        resultados = []
        for cupo in cupos:
            contador_aciertos = asignada.filter(sala_id=cupo.id).count()
            resultados.append({"cupo": cupo, "aciertos": contador_aciertos})

        context["object"] = Vacantes.objects.get(pk=self.kwargs["pk"])
        context["admi"] = admi
        context["admi2"] = admi2
        context["cupos"] = cupos
        context["asignada"] = asignada
        context["resultados"] = resultados
        context["ivi"] = ivi
        return context


class CDIFIntervencionesCreateView(PermisosMixin, CreateView):
    permission_required = "Usuarios.programa_CDIF"
    model = CDIF_Intervenciones  # Debería ser el modelo CDIF_Intervenciones
    template_name = "SIF_CDIF/intervenciones_form.html"
    form_class = CDIF_IntervencionesForm

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "CDIF  Administrador",
            "CDIF  Directivo",
            "CDIF  Equipo operativo",
            # "CDIF  Equipo técnico",
            # "CDIF  Consultante",
            # "CDIF  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa Administración
        grupos_usuario = request.user.groups.filter(name__startswith="CDIF")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

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

        return redirect("CDIF_intervencion_ver", self.object.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = CDIF_Admision.objects.get(
            pk=self.kwargs["pk"]
        )  # Obtén el objeto directamente
        context["form"] = self.get_form()  # Obtiene una instancia del formulario
        context["criterios_ivi"] = Criterios_IVI.objects.all()

        return context


class CDIFIntervencionesUpdateView(PermisosMixin, UpdateView):
    permission_required = "Usuarios.programa_CDIF"
    model = CDIF_Intervenciones
    template_name = "SIF_CDIF/intervenciones_form.html"
    form_class = CDIF_IntervencionesForm

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "CDIF  Administrador",
            "CDIF  Directivo",
            # "CDIF  Equipo operativo",
            # "CDIF  Equipo técnico",
            # "CDIF  Consultante",
            # "CDIF  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa Administración
        grupos_usuario = request.user.groups.filter(name__startswith="CDIF")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

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

        return redirect("CDIF_intervencion_ver", self.object.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = CDIF_Intervenciones.objects.filter(pk=self.kwargs["pk"]).first()
        admi = CDIF_Admision.objects.filter(id=pk.fk_admision.id).first()

        context["object"] = admi

        return context


class CDIFIntervencionesLegajosListView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_CDIF"
    template_name = "SIF_CDIF/intervenciones_legajo_list.html"
    model = CDIF_Admision

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        admi = CDIF_Admision.objects.filter(pk=self.kwargs["pk"]).first()
        lastVO = CDIF_VacantesOtorgadas.objects.filter(fk_admision_id=admi.id).last()
        intervenciones = CDIF_Intervenciones.objects.filter(
            fk_admision_id=admi.id
        ).all()
        intervenciones_last = CDIF_Intervenciones.objects.filter(
            fk_admision_id=admi.id
        ).last()
        preadmi = CDIF_PreAdmision.objects.filter(pk=admi.fk_preadmi_id).first()
        criterio = CDIF_IndiceIVI.objects.filter(fk_preadmi_id=preadmi, tipo="Ingreso")
        if criterio:
            observaciones = CDIF_Foto_IVI.objects.filter(
                clave=criterio.first().clave, tipo="Ingreso"
            ).first()
        else:
            observaciones = ""
        criterio2 = CDIF_IndiceIVI.objects.filter(fk_preadmi_id=preadmi, tipo="Ingreso")
        if criterio2:
            observaciones2 = CDIF_Foto_IVI.objects.filter(
                clave=criterio2.last().clave, tipo="Ingreso"
            ).first()
        else:
            observaciones2 = ""

        context["object"] = admi
        context["lastvo"] = lastVO
        context["intervenciones"] = intervenciones
        context["intervenciones_count"] = intervenciones.count()
        context["intervenciones_last"] = intervenciones_last

        context["puntaje"] = criterio.aggregate(total=Sum("fk_criterios_ivi__puntaje"))
        context["observaciones"] = observaciones
        context["observaciones2"] = observaciones2
        context["puntaje2"] = criterio2.aggregate(
            total=Sum("fk_criterios_ivi__puntaje")
        )

        return context


class CDIFIntervencionesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.programa_CDIF"
    template_name = "SIF_CDIF/intervenciones_list.html"
    model = CDIF_Intervenciones

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "CDIF  Administrador",
            "CDIF  Directivo",
            "CDIF  Equipo operativo",
            "CDIF  Equipo técnico",
            "CDIF  Consultante",
            # "CDIF  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa Administración
        grupos_usuario = request.user.groups.filter(name__startswith="CDIF")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        intervenciones = CDIF_Intervenciones.objects.all()
        context["intervenciones"] = intervenciones
        return context


class CDIFIntervencionesDetail(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_CDIF"
    template_name = "SIF_CDIF/intervencion_detail.html"
    model = CDIF_Intervenciones


class CDIFOpcionesResponsablesCreateView(PermisosMixin, CreateView):
    permission_required = "Usuarios.programa_CDIF"
    template_name = "SIF_CDIF/intervenciones_resposables.html"
    model = OpcionesResponsables
    form_class = CDIF_OpcionesResponsablesForm

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse("CDIF_OpcionesResponsables"))


class CDIFIntervencionesDeleteView(PermisosMixin, DeleteView):
    permission_required = "Usuarios.programa_CDIF"
    model = CDIF_Intervenciones
    template_name = "SIF_CDIF/intervenciones_confirm_delete.html"
    success_url = reverse_lazy("CDIF_intervenciones_listar")

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "CDIF  Administrador",
            # "CDIF  Directivo",
            # "CDIF  Equipo operativo",
            # "CDIF  Equipo técnico",
            # "CDIF  Consultante",
            # "CDIF  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa Administración
        grupos_usuario = request.user.groups.filter(name__startswith="CDIF")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

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


class CDIFAdmisionesBuscarListView(PermisosMixin, TemplateView):
    permission_required = "Usuarios.programa_CDIF"
    template_name = "SIF_CDIF/admisiones_buscar.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        object_list = CDIF_PreAdmision.objects.none()
        mostrar_resultados = False
        mostrar_btn_resetear = False
        query = self.request.GET.get("busqueda")
        if query:
            object_list = (
                CDIF_Admision.objects.filter(
                    Q(fk_preadmi__fk_legajo__apellido__iexact=query)
                    | Q(fk_preadmi__fk_legajo__documento__iexact=query),
                    fk_preadmi__fk_derivacion__fk_programa_id=settings.PROG_CDIF,
                )
                .exclude(estado__in=["Rechazada", "Aceptada"])
                .distinct()
            )
            if not object_list:
                messages.warning(self.request, ("La búsqueda no arrojó resultados."))

            mostrar_btn_resetear = True
            mostrar_resultados = True

        context["mostrar_resultados"] = mostrar_resultados
        context["mostrar_btn_resetear"] = mostrar_btn_resetear
        context["object_list"] = object_list

        return self.render_to_response(context)


class CDIFIndiceIviEgresoCreateView(PermisosMixin, CreateView):
    permission_required = "Usuarios.programa_CDIF"
    model = Legajos
    template_name = "SIF_CDIF/indiceivi_form_egreso.html"
    form_class = CDIF_IndiceIviForm
    success_url = reverse_lazy("legajos_listar")

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        admi = CDIF_Admision.objects.filter(pk=pk).first()
        object = Legajos.objects.filter(pk=admi.fk_preadmi.fk_legajo.id).first()
        criterio = Criterios_IVI.objects.all()
        context["object"] = object
        context["criterio"] = criterio
        context["form2"] = CDIF_IndiceIviHistorialForm()
        context["admi"] = admi
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        admi = CDIF_Admision.objects.filter(pk=pk).first()
        # Genera una clave única utilizando uuid4 (versión aleatoria)
        preadmi = CDIF_PreAdmision.objects.filter(
            fk_legajo_id=admi.fk_preadmi.fk_legajo.id
        ).first()
        foto_ivi = CDIF_Foto_IVI.objects.filter(fk_preadmi_id=preadmi.id).first()
        clave = foto_ivi.clave
        nombres_campos = request.POST.keys()
        print(nombres_campos)
        puntaje_maximo = Criterios_IVI.objects.aggregate(total=Sum("puntaje"))["total"]
        total_puntaje = 0
        historico = HistorialLegajoIndices()
        for f in nombres_campos:
            if f.isdigit():
                criterio_ivi = Criterios_IVI.objects.filter(id=f).first()
                # Sumar el valor de f al total_puntaje
                total_puntaje += int(criterio_ivi.puntaje)
                base = CDIF_IndiceIVI()
                base.fk_criterios_ivi_id = f
                base.fk_legajo_id = admi.fk_preadmi.fk_legajo.id
                base.fk_preadmi_id = preadmi.id
                base.tipo = "Egreso"
                base.presencia = True
                base.programa = "CDIF"
                historico.programa = base.programa
                base.clave = clave
                base.save()

        # total_puntaje contiene la suma de los valores de F
        foto = CDIF_Foto_IVI()
        foto.observaciones = request.POST.get("observaciones", "")
        foto.fk_preadmi_id = preadmi.id
        foto.fk_legajo_id = preadmi.fk_legajo_id
        foto.puntaje = total_puntaje
        foto.puntaje_max = puntaje_maximo
        # foto.crit_modificables = crit_modificables
        # foto.crit_presentes = crit_presentes
        foto.tipo = "Egreso"
        foto.clave = clave
        foto.creado_por_id = self.request.user.id

        historico.observaciones = foto.observaciones
        historico.fk_legajo_id = preadmi.fk_legajo_id
        historico.puntaje = total_puntaje
        historico.puntaje_total = total_puntaje
        historico.puntaje_max = puntaje_maximo
        historico.tipo = "Egreso"
        historico.clave = clave

        historico.save()

        foto.save()

        admi.estado = "Inactiva"
        admi.inactiva_motivo_baja = request.POST.get("detalle_de_baja", "")
        admi.inactiva_tipo_baja = request.POST.get("tipo_de_baja", "")
        admi.modificado_por_id = self.request.user.id
        admi.save()

        # ---------HISTORIAL---------------------------------
        pk = self.kwargs["pk"]
        legajo = admi.fk_preadmi
        base = CDIF_Historial()
        base.fk_legajo_id = legajo.fk_legajo.id
        base.fk_legajo_derivacion_id = legajo.fk_derivacion_id
        base.fk_preadmi_id = legajo.id
        base.movimiento = "IVI EGRESO"
        base.creado_por_id = self.request.user.id
        base.save()

        return redirect("CDIF_admisiones_listar")
