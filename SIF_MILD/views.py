from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    TemplateView,
    FormView,
)
from Legajos.models import LegajosDerivaciones, HistorialLegajoIndices
from Legajos.forms import (
    DerivacionesRechazoForm,
    LegajosDerivacionesForm,
    NuevoLegajoFamiliarForm,
)
from django.db.models import Q
from .models import *
from Configuraciones.models import *
from .forms import *
from Usuarios.mixins import PermisosMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, QueryDict
from django.db.models import Sum, F, ExpressionWrapper, IntegerField, Count, Max
import uuid
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from SIF_CDIF.models import Criterios_IVI
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from Legajos.models import LegajoAlertas


# # Create your views here.
# derivaciones = LegajosDerivaciones.objects.filter(m2m_programas__nombr__iexact="MILD")
# print(derivaciones)


def obtener_rol(request):
    if request.user.is_authenticated:
        # Supongamos que este método retorna los roles del usuario
        return list(request.user.groups.values_list("name", flat=True))
    return []


class MILDDerivacionesBuscarListView(TemplateView, PermisosMixin):
    permission_required = "Usuarios.programa_1000D"
    template_name = "SIF_MILD/derivaciones_buscar.html"

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
                "1000D  Administrador",
                "1000D  Directivo",
                "1000D  Equipo operativo",
                "1000D  Equipo técnico",
                "1000D  Consultante",
                # "1000D  Observador",
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


class MILDDerivacionesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.programa_1000D"
    template_name = "SIF_MILD/derivaciones_bandeja_list.html"
    queryset = LegajosDerivaciones.objects.filter(fk_programa=settings.PROG_MILD)

    def get_context_data(self, **kwargs):
        context = super(MILDDerivacionesListView, self).get_context_data(**kwargs)
        model = self.queryset

        query = self.request.GET.get("busqueda")

        if query:
            object_list = LegajosDerivaciones.objects.filter(
                (
                    Q(fk_legajo__apellido__iexact=query)
                    | Q(fk_legajo__nombre__iexact=query)
                )
                & Q(fk_programa=settings.PROG_MILD)
            ).distinct()
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


class MILDDerivacionesDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_1000D"
    template_name = "SIF_MILD/derivaciones_detail.html"
    model = LegajosDerivaciones

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(
            pk=pk, fk_programa=settings.PROG_MILD
        ).first()
        ivi = MILD_IndiceIVI.objects.filter(fk_legajo_id=legajo.fk_legajo_id)
        resultado = (
            ivi.values("clave", "creado", "programa")
            .annotate(total=Sum("fk_criterios_ivi__puntaje"))
            .order_by("-creado")
        )
        preadmi = MILD_PreAdmision.objects.filter(fk_derivacion_id=pk).first()

        if preadmi:
            context["acompaniante_asignado"] = preadmi.acompaniante_asignado
            context["acompaniante_entrevista"] = preadmi.acompaniante_entrevista

        context["archivos"] = LegajosDerivacionesArchivos.objects.filter(
            legajo_derivacion=pk
        )

        rol = obtener_rol(self.request)
        roles_permitidos = [
            "1000D  Administrador",
            "1000D  Directivo",
            # "1000D  Equipo operativo",
            "1000D  Equipo operativo",
            # "1000D  Consultante",
            # "1000D  Observador",
        ]
        if self.request.user.is_superuser or any(
            role in roles_permitidos for role in rol
        ):
            context["btn_aceptar"] = True
        else:
            context["btn_aceptar"] = False

        roles_permitidos_rechazar = [
            "1000D  Administrador",
            "1000D  Directivo",
            # "1000D  Equipo operativo",
            "1000D  Equipo operativo",
            # "1000D  Consultante",
            # "1000D  Observador",
        ]
        if self.request.user.is_superuser or any(
            role in roles_permitidos_rechazar for role in rol
        ):
            context["btn_rechazar"] = True
        else:
            context["btn_rechazar"] = False

        roles_permitidos_eliminar_editar = [
            "1000D  Administrador",
            # "1000D  Directivo",
            # "1000D  Equipo operativo",
            # "1000D  Equipo operativo",
            # "1000D  Consultante",
            # "1000D  Observador",
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
        return context


class MILDDerivacionesRechazo(PermisosMixin, CreateView):
    permission_required = "Usuarios.programa_1000D"
    template_name = "SIF_MILD/derivaciones_rechazo.html"
    form_class = DerivacionesRechazoForm

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "1000D  Administrador",
            "1000D  Directivo",
            # "1000D  Equipo operativo",
            "1000D  Equipo técnico",
            # "1000D  Consultante",
            # "1000D  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa 1000D
        grupos_usuario = request.user.groups.filter(name__startswith="1000D")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(
            pk=pk, fk_programa=settings.PROG_MILD
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
        return HttpResponseRedirect(reverse("MILD_derivaciones_listar"))

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("MILD_derivaciones_listar")


class MILDDerivacionesUpdateView(PermisosMixin, UpdateView):
    permission_required = "Usuarios.programa_1000D"
    model = LegajosDerivaciones
    template_name = "SIF_MILD/derivaciones_form.html"
    form_class = LegajosDerivacionesForm
    success_message = "Derivación editada con éxito"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "1000D  Administrador",
            # "1000D  Directivo",
            # "1000D  Equipo operativo",
            # "1000D  Equipo técnico",
            # "1000D  Consultante",
            # "1000D  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa 1000D
        grupos_usuario = request.user.groups.filter(name__startswith="1000D")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def get_initial(self):
        initial = super().get_initial()
        initial["fk_usuario"] = self.request.user
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        delete_files = self.request.POST.getlist("delete_files")

        if delete_files:
            archivos = LegajosDerivacionesArchivos.objects.filter(id__in=delete_files)
            archivos.delete()

        return response

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

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("MILD_derivaciones_ver", kwargs={"pk": pk})


class MILDPreAdmisionesCreateView(PermisosMixin, CreateView, SuccessMessageMixin):
    permission_required = "Usuarios.programa_1000D"
    template_name = "SIF_MILD/preadmisiones_form.html"
    model = MILD_PreAdmision
    form_class = MILD_PreadmisionesForm
    form_nuevo_grupo_familiar_class = NuevoLegajoFamiliarForm()
    success_message = "Preadmisión creada correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "1000D  Administrador",
            "1000D  Directivo",
            "1000D  Equipo operativo",
            "1000D  Equipo técnico",
            # "1000D  Consultante",
            # "1000D  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa 1000D
        grupos_usuario = request.user.groups.filter(name__startswith="1000D")

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
        familia_inversa = LegajoGrupoFamiliar.objects.filter(
            fk_legajo_1_id=legajo.fk_legajo_id
        )
        context["pk"] = pk
        context["legajo"] = legajo
        context["familia"] = familia
        context["nuevo_grupo_familiar_form"] = self.form_nuevo_grupo_familiar_class
        context["familia_inversa"] = familia_inversa
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
        # return HttpResponseRedirect(reverse('MILD_preadmisiones_editar', args=[self.object.pk]))

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
        base = MILD_Historial()
        base.fk_legajo_id = legajo.fk_legajo.id
        base.fk_legajo_derivacion_id = pk
        base.fk_preadmi_id = self.object.id
        base.movimiento = "ACEPTADO A PREADMISION"
        base.creado_por_id = self.request.user.id
        base.save()

        return HttpResponseRedirect(
            reverse("MILD_preadmisiones_ver", args=[self.object.pk])
        )


class MILDPreAdmisionesUpdateView(PermisosMixin, UpdateView, SuccessMessageMixin):
    permission_required = "Usuarios.programa_1000D"
    template_name = "SIF_MILD/preadmisiones_form.html"
    model = MILD_PreAdmision
    form_class = MILD_PreadmisionesForm
    form_nuevo_grupo_familiar_class = NuevoLegajoFamiliarForm()
    success_message = "Preadmisión creada correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "1000D  Administrador",
            "1000D  Directivo",
            "1000D  Equipo operativo",
            "1000D  Equipo técnico",
            # "1000D  Consultante",
            # "1000D  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa 1000D
        grupos_usuario = request.user.groups.filter(name__startswith="1000D")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        if "conviven" in self.request.POST:
            self.crear_grupo_hogar(self.request.POST)
            messages.success(self.request, "Familiar agregado correctamente.")
        pk = MILD_PreAdmision.objects.filter(pk=self.kwargs["pk"]).first()
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(pk=pk.fk_derivacion_id).first()
        familia = LegajoGrupoFamiliar.objects.filter(fk_legajo_2_id=legajo.fk_legajo_id)
        familia_inversa = LegajoGrupoFamiliar.objects.filter(
            fk_legajo_1_id=legajo.fk_legajo_id
        )

        context["pk"] = pk.fk_derivacion_id
        context["legajo"] = legajo
        context["familia"] = familia
        context["familia_inversa"] = familia_inversa
        context["nuevo_grupo_familiar_form"] = self.form_nuevo_grupo_familiar_class
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
        # return HttpResponseRedirect(reverse('MILD_preadmisiones_editar', args=[self.object.pk]))

    def form_valid(self, form):
        pk = MILD_PreAdmision.objects.filter(pk=self.kwargs["pk"]).first()
        form.instance.creado_por_id = pk.creado_por_id
        form.instance.vinculo1 = form.cleaned_data["vinculo1"]
        form.instance.vinculo2 = form.cleaned_data["vinculo2"]
        form.instance.vinculo3 = form.cleaned_data["vinculo3"]
        form.instance.vinculo4 = form.cleaned_data["vinculo4"]
        form.instance.vinculo5 = form.cleaned_data["vinculo5"]
        form.instance.estado = pk.estado
        form.instance.modificado_por_id = self.request.user.id
        self.object = form.save()

        return HttpResponseRedirect(
            reverse("MILD_preadmisiones_ver", args=[self.object.pk])
        )


class MILDPreAdmisionesDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_1000D"
    template_name = "SIF_MILD/preadmisiones_detail.html"
    model = MILD_PreAdmision

    def get_context_data(self, **kwargs):
        pk = MILD_PreAdmision.objects.filter(pk=self.kwargs["pk"]).first()
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(pk=pk.fk_derivacion_id).first()
        familia = LegajoGrupoFamiliar.objects.filter(fk_legajo_2_id=legajo.fk_legajo_id)
        ivi = MILD_IndiceIVI.objects.filter(fk_legajo_id=legajo.fk_legajo_id)
        ingreso = MILD_IndiceIngreso.objects.filter(fk_legajo_id=legajo.fk_legajo_id)
        resultado = (
            ivi.values("clave", "creado", "programa")
            .annotate(total=Sum("fk_criterios_ivi__puntaje"))
            .order_by("-creado")
        )
        resultado_ingreso = (
            ingreso.values("clave", "creado", "programa")
            .annotate(total=Sum("fk_criterios_ingreso__puntaje"))
            .order_by("-creado")
        )
        print(resultado_ingreso)
        rol = obtener_rol(self.request)
        roles_permitidos = [
            "1000D  Administrador",
            "1000D  Directivo",
            "1000D  Equipo operativo",
            "1000D  Equipo operativo",
            # "1000D  Consultante",
            # "1000D  Observador",
        ]
        if self.request.user.is_superuser or any(
            role in roles_permitidos for role in rol
        ):
            context["btn_admitir"] = True
        else:
            context["btn_admitir"] = False

        roles_rechazo = [
            "1000D  Administrador",
            "1000D  Directivo",
            # "1000D  Equipo operativo",
            "1000D  Equipo operativo",
            # "1000D  Consultante",
            # "1000D  Observador",
        ]
        if self.request.user.is_superuser or any(role in roles_rechazo for role in rol):
            context["btn_rechazar"] = True
        else:
            context["btn_rechazar"] = False

        context["ivi"] = ivi
        context["ingreso"] = ingreso
        context["criterios_total"] = ingreso.count()
        context["cant_sanitarios"] = ingreso.filter(
            fk_criterios_ingreso__tipo="Criterios sanitarios para el ingreso"
        ).count()
        context["cant_sociales"] = ingreso.filter(
            fk_criterios_ingreso__tipo="Criterios sociales para el ingreso"
        ).count()
        context["autonomos"] = ingreso.filter(
            fk_criterios_ingreso__tipo="Criteros autónomos de ingreso"
        ).all()
        context["resultado"] = resultado
        context["resultado_ingreso"] = resultado_ingreso
        context["legajo"] = legajo
        context["familia"] = familia
        return context

    def post(self, request, *args, **kwargs):
        if "finalizar_preadm" in request.POST:
            # Realiza la actualización del campo aquí
            objeto = self.get_object()
            objeto.estado = "Pendiente"
            objeto.ivi = "NO"
            objeto.indice_ingreso = "NO"
            objeto.admitido = "NO"
            objeto.save()

            # ---------HISTORIAL---------------------------------
            pk = self.kwargs["pk"]
            legajo = MILD_PreAdmision.objects.filter(pk=pk).first()
            base = MILD_Historial()
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
            legajo = MILD_PreAdmision.objects.filter(pk=pk).first()
            base = MILD_Historial()
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
            legajo = MILD_PreAdmision.objects.filter(pk=pk).first()
            base = MILD_Historial()
            base.fk_legajo_id = legajo.fk_legajo.id
            base.fk_legajo_derivacion_id = legajo.fk_derivacion_id
            base.fk_preadmi_id = pk
            base.movimiento = "Rechazado"
            base.creado_por_id = self.request.user.id
            base.save()
            # Redirige de nuevo a la vista de detalle actualizada
            return HttpResponseRedirect(self.request.path_info)


class MILDPreAdmisionesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.programa_1000D"
    template_name = "SIF_MILD/preadmisiones_list.html"
    model = MILD_PreAdmision

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "1000D  Administrador",
            "1000D  Directivo",
            "1000D  Equipo operativo",
            "1000D  Equipo técnico",
            "1000D  Consultante",
            # "1000D  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa 1000D
        grupos_usuario = request.user.groups.filter(name__startswith="1000D")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pre_admi = MILD_PreAdmision.objects.all()
        context["object"] = pre_admi
        return context


class MILDPreAdmisionesBuscarListView(PermisosMixin, TemplateView):
    permission_required = "Usuarios.programa_1000D"
    template_name = "SIF_MILD/preadmisiones_buscar.html"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "1000D  Administrador",
            "1000D  Directivo",
            "1000D  Equipo operativo",
            "1000D  Equipo técnico",
            "1000D  Consultante",
            # "1000D  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa 1000D
        grupos_usuario = request.user.groups.filter(name__startswith="1000D")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        object_list = MILD_PreAdmision.objects.none()
        mostrar_resultados = False
        mostrar_btn_resetear = False
        query = self.request.GET.get("busqueda")
        if query:
            object_list = (
                MILD_PreAdmision.objects.filter(
                    Q(fk_legajo__apellido__iexact=query)
                    | Q(fk_legajo__documento__iexact=query),
                    fk_derivacion__fk_programa_id=settings.PROG_MILD,
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


class MILDPreAdmisionesDeleteView(PermisosMixin, DeleteView):
    permission_required = "Usuarios.programa_1000D"
    model = MILD_PreAdmision
    template_name = "SIF_MILD/preadmisiones_confirm_delete.html"
    success_url = reverse_lazy("MILD_preadmisiones_listar")

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "1000D  Administrador",
            # "1000D  Directivo",
            # "1000D  Equipo operativo",
            # "1000D  Equipo técnico",
            # "1000D  Consultante",
            # "1000D  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa 1000D
        grupos_usuario = request.user.groups.filter(name__startswith="1000D")

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

            return redirect("MILD_preadmisiones_ver", pk=int(self.object.id))

        if self.request.user.id != self.object.creado_por.id:
            messages.error(
                self.request,
                "Solo el usuario que generó esta derivación puede eliminarla.",
            )

            return redirect("MILD_preadmisiones_ver", pk=int(self.object.id))

        else:
            self.object.delete()
            return redirect(self.success_url)


class MILDCriteriosIngresoCreateView(PermisosMixin, CreateView):
    permission_required = "Usuarios.programa_1000D"
    template_name = "SIF_MILD/criterios_ingreso_form.html"
    model = Criterios_Ingreso
    form_class = criterios_Ingreso

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse("MILD_criterios_ingreso_crear"))


class MILDIndiceIngresoCreateView(PermisosMixin, CreateView):
    permission_required = "Usuarios.programa_1000D"
    model = Criterios_Ingreso
    template_name = "SIF_MILD/indiceingreso_form.html"
    form_class = MILD_IndiceIngresoForm

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "1000D  Administrador",
            "1000D  Directivo",
            "1000D  Equipo operativo",
            "1000D  Equipo técnico",
            # "1000D  Consultante",
            # "1000D  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa 1000D
        grupos_usuario = request.user.groups.filter(name__startswith="1000D")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        object = MILD_PreAdmision.objects.filter(pk=pk).first()
        # object = Legajos.objects.filter(pk=pk).first()
        criterio = Criterios_Ingreso.objects.all()
        context["object"] = object
        context["criterio"] = criterio
        context["form2"] = MILD_IndiceIngresoHistorialForm()
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        # Genera una clave única utilizando uuid4 (versión aleatoria)
        preadmi = MILD_PreAdmision.objects.filter(pk=pk).first()
        clave = str(uuid.uuid4())
        nombres_campos = request.POST.keys()
        puntaje_maximo = Criterios_Ingreso.objects.aggregate(total=Sum("puntaje"))[
            "total"
        ]
        total_puntaje = 0
        historico = HistorialLegajoIndices()

        # ----------------------------------
        # # valida que por lomenos un criterio este seleciconado
        # validacion = False
        # for f in nombres_campos:
        #     if f.isdigit():
        #         criterio_ingreso = Criterios_Ingreso.objects.filter(id=f).first()
        #         if criterio_ingreso.tipo == "Criterios sanitarios para el ingreso":
        #             validacion = True
        #             break

        # if not validacion:
        #     messages.error(
        #         self.request, "Debe seleccionar al menos un criterio sanitario."
        #     )
        #     return redirect("MILD_indiceingreso_crear", pk)
        # ----------------------------------

        for f in nombres_campos:
            if f.isdigit():
                criterio_ingreso = Criterios_Ingreso.objects.filter(id=f).first()
                # Sumar el valor de f al total_puntaje
                total_puntaje += int(criterio_ingreso.puntaje)
                base = MILD_IndiceIngreso()
                base.fk_criterios_ingreso_id = f
                base.fk_legajo_id = preadmi.fk_legajo_id
                base.fk_preadmi_id = pk
                base.tipo = "Ingreso"
                base.presencia = True
                base.programa = "MILD"
                historico.programa = base.programa
                base.clave = clave
                base.save()

        # total_puntaje contiene la suma de los valores de F
        foto = MILD_Foto_Ingreso()
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

        preadmi.indice_ingreso = "SI"
        preadmi.save()

        # ---------HISTORIAL---------------------------------
        pk = self.kwargs["pk"]
        base = MILD_Historial()
        base.fk_legajo_id = preadmi.fk_legajo.id
        base.fk_legajo_derivacion_id = preadmi.fk_derivacion_id
        base.fk_preadmi_id = preadmi.id
        base.movimiento = "CREACION INDICE INGRESO"
        base.creado_por_id = self.request.user.id
        base.save()

        return redirect("MILD_indiceingreso_ver", preadmi.id)


class MILDIndiceIngresoUpdateView(PermisosMixin, UpdateView):
    permission_required = "Usuarios.programa_1000D"
    template_name = "SIF_MILD/indiceingreso_edit.html"
    model = MILD_PreAdmision
    form_class = MILD_IndiceIngresoForm

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "1000D  Administrador",
            # "1000D  Directivo",
            "1000D  Equipo operativo",
            # "1000D  Equipo técnico",
            # "1000D  Consultante",
            # "1000D  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa 1000D
        grupos_usuario = request.user.groups.filter(name__startswith="1000D")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        activos = MILD_IndiceIngreso.objects.filter(fk_preadmi_id=pk)
        observaciones = MILD_Foto_Ingreso.objects.filter(fk_preadmi_id=pk).first()

        context = super().get_context_data(**kwargs)
        context["object"] = MILD_PreAdmision.objects.filter(pk=pk).first()
        context["activos"] = activos
        context["clave"] = observaciones.clave
        context["observaciones"] = observaciones.observaciones
        context["criterio"] = Criterios_Ingreso.objects.all()
        context["form2"] = MILD_IndiceIngresoHistorialForm()
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        preadmi = MILD_PreAdmision.objects.filter(pk=pk).first()
        MILD_foto = MILD_Foto_IVI.objects.filter(fk_preadmi_id=pk).first()
        clave = MILD_foto.clave
        indices_ingreso = MILD_IndiceIngreso.objects.filter(clave=clave)
        # MILD_foto.delete()
        indices_ingreso.delete()
        nombres_campos = request.POST.keys()
        puntaje_maximo = Criterios_Ingreso.objects.aggregate(total=Sum("puntaje"))[
            "total"
        ]
        total_puntaje = 0
        historico = HistorialLegajoIndices()
        for f in nombres_campos:
            if f.isdigit():
                criterio_ingreso = Criterios_Ingreso.objects.filter(id=f).first()
                # Sumar el valor de f al total_puntaje
                total_puntaje += int(criterio_ingreso.puntaje)
                base = MILD_IndiceIVI()
                base.fk_criterios_ingreso_id = f
                base.fk_legajo_id = preadmi.fk_legajo_id
                base.fk_preadmi_id = pk
                base.presencia = True
                base.programa = "MILD"
                historico.programa = base.programa
                base.clave = clave
                base.save()

        # total_puntaje contiene la suma de los valores de F
        foto = MILD_Foto_Ingreso.objects.filter(clave=clave).first()
        foto.observaciones = request.POST.get("observaciones", "")
        foto.fk_preadmi_id = pk
        foto.fk_legajo_id = preadmi.fk_legajo_id
        foto.puntaje = total_puntaje
        foto.puntaje_max = puntaje_maximo
        # foto.crit_modificables = crit_modificables
        # foto.crit_presentes = crit_presentes
        # foto.tipo = "Ingreso"
        # foto.clave = clave
        foto.modificado_por_id = self.request.user.id

        historico.observaciones = foto.observaciones
        historico.fk_legajo_id = preadmi.fk_legajo_id
        historico.puntaje = total_puntaje
        historico.puntaje_total = total_puntaje
        historico.puntaje_max = puntaje_maximo
        historico.tipo = "Ingreso"
        historico.clave = clave

        historico.save()
        foto.save()

        # ---------HISTORIAL---------------------------------
        pk = self.kwargs["pk"]
        preadmi = MILD_PreAdmision.objects.filter(pk=pk).first()
        base = MILD_Historial()
        base.fk_legajo_id = preadmi.fk_legajo.id
        base.fk_legajo_derivacion_id = preadmi.fk_derivacion_id
        base.fk_preadmi_id = preadmi.id
        base.movimiento = "MODIFICACION INDICE INGRESO"
        base.creado_por_id = self.request.user.id
        base.save()

        return redirect("MILD_indiceingreso_ver", preadmi.id)


class MILDIndiceIngresoDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_1000D"
    template_name = "SIF_MILD/indiceingreso_detail.html"
    model = MILD_PreAdmision

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        criterio = MILD_IndiceIngreso.objects.filter(fk_preadmi_id=pk, tipo="Ingreso")
        object = MILD_PreAdmision.objects.filter(pk=pk).first()
        foto_ingreso = MILD_Foto_Ingreso.objects.filter(
            fk_preadmi_id=pk, tipo="Ingreso"
        ).first()

        context["object"] = object
        context["foto_ingreso"] = foto_ingreso
        context["criterio"] = criterio
        context["puntaje"] = criterio.aggregate(
            total=Sum("fk_criterios_ingreso__puntaje")
        )
        context["cantidad"] = criterio.count()
        context["cant_sanitarios"] = criterio.filter(
            fk_criterios_ingreso__tipo="Criterios sanitarios para el ingreso"
        ).count()
        context["cant_sociales"] = criterio.filter(
            fk_criterios_ingreso__tipo="Criterios sociales para el ingreso"
        ).count()
        context["mod_puntaje"] = criterio.filter(
            fk_criterios_ingreso__modificable__iexact="SI"
        ).aggregate(total=Sum("fk_criterios_ingreso__puntaje"))
        context["ajustes"] = criterio.filter(
            fk_criterios_ingreso__tipo="Ajustes"
        ).count()
        # context['maximo'] = foto_ingreso.puntaje_max
        return context


# --------- CREAR IVI -------------------------------------


class MILDCriteriosIVICreateView(PermisosMixin, CreateView):
    permission_required = "Usuarios.programa_1000D"
    template_name = "SIF_MILD/criterios_ivi_form.html"
    model = Criterios_IVI
    form_class = criterios_IVI

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse("MILD_criterios_ivi_crear"))


class MILDIndiceIviCreateView(PermisosMixin, CreateView):
    permission_required = "Usuarios.programa_1000D"
    model = Criterios_IVI
    template_name = "SIF_MILD/indiceivi_form.html"
    form_class = MILD_IndiceIviForm

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "1000D  Administrador",
            "1000D  Directivo",
            "1000D  Equipo operativo",
            "1000D  Equipo técnico",
            # "1000D  Consultante",
            # "1000D  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa 1000D
        grupos_usuario = request.user.groups.filter(name__startswith="1000D")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        object = MILD_PreAdmision.objects.filter(pk=pk).first()
        # object = Legajos.objects.filter(pk=pk).first()
        criterio = Criterios_IVI.objects.all()
        context["object"] = object
        context["criterio"] = criterio
        context["form2"] = MILD_IndiceIviHistorialForm()
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        # Genera una clave única utilizando uuid4 (versión aleatoria)
        preadmi = MILD_PreAdmision.objects.filter(pk=pk).first()
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
                base = MILD_IndiceIVI()
                base.fk_criterios_ivi_id = f
                base.fk_legajo_id = preadmi.fk_legajo_id
                base.fk_preadmi_id = pk
                base.tipo = "Ingreso"
                base.presencia = True
                base.programa = "MILD"
                historico.programa = base.programa
                base.clave = clave
                base.save()

        # total_puntaje contiene la suma de los valores de F
        foto = MILD_Foto_IVI()
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
        base = MILD_Historial()
        base.fk_legajo_id = preadmi.fk_legajo.id
        base.fk_legajo_derivacion_id = preadmi.fk_derivacion_id
        base.fk_preadmi_id = preadmi.id
        base.movimiento = "CREACION IVI"
        base.creado_por_id = self.request.user.id
        base.save()

        return redirect("MILD_indiceivi_ver", preadmi.id)


class MILDIndiceIviUpdateView(PermisosMixin, UpdateView):
    permission_required = "Usuarios.programa_1000D"
    template_name = "SIF_MILD/indiceivi_edit.html"
    model = MILD_PreAdmision
    form_class = MILD_IndiceIviForm

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "1000D  Administrador",
            # "1000D  Directivo",
            "1000D  Equipo operativo",
            # "1000D  Equipo técnico",
            # "1000D  Consultante",
            # "1000D  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa 1000D
        grupos_usuario = request.user.groups.filter(name__startswith="1000D")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        activos = MILD_IndiceIVI.objects.filter(fk_preadmi_id=pk)
        observaciones = MILD_Foto_IVI.objects.filter(fk_preadmi_id=pk).first()

        context = super().get_context_data(**kwargs)
        context["object"] = MILD_PreAdmision.objects.filter(pk=pk).first()
        context["activos"] = activos
        context["clave"] = observaciones.clave
        context["observaciones"] = observaciones.observaciones
        context["criterio"] = Criterios_IVI.objects.all()
        context["form2"] = MILD_IndiceIviHistorialForm()
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        preadmi = MILD_PreAdmision.objects.filter(pk=pk).first()
        MILD_foto = MILD_Foto_IVI.objects.filter(fk_preadmi_id=pk).first()
        clave = MILD_foto.clave
        indices_ivi = MILD_IndiceIVI.objects.filter(clave=clave)
        # MILD_foto.delete()
        indices_ivi.delete()
        nombres_campos = request.POST.keys()
        puntaje_maximo = Criterios_IVI.objects.aggregate(total=Sum("puntaje"))["total"]
        total_puntaje = 0
        historico = HistorialLegajoIndices()
        for f in nombres_campos:
            if f.isdigit():
                criterio_ivi = Criterios_IVI.objects.filter(id=f).first()
                # Sumar el valor de f al total_puntaje
                total_puntaje += int(criterio_ivi.puntaje)
                base = MILD_IndiceIVI()
                base.fk_criterios_ivi_id = f
                base.fk_legajo_id = preadmi.fk_legajo_id
                base.fk_preadmi_id = pk
                base.tipo = "Ingreso"
                base.presencia = True
                base.programa = "MILD"
                historico.programa = base.programa
                base.clave = clave
                base.save()

        # total_puntaje contiene la suma de los valores de F
        foto = MILD_Foto_IVI.objects.filter(clave=clave).first()
        foto.observaciones = request.POST.get("observaciones", "")
        foto.fk_preadmi_id = pk
        foto.fk_legajo_id = preadmi.fk_legajo_id
        foto.puntaje = total_puntaje
        foto.puntaje_max = puntaje_maximo
        # foto.crit_modificables = crit_modificables
        # foto.crit_presentes = crit_presentes
        # foto.tipo = "Ingreso"
        # foto.clave = clave
        foto.modificado_por_id = self.request.user.id

        historico.observaciones = foto.observaciones
        historico.fk_legajo_id = preadmi.fk_legajo_id
        historico.puntaje = total_puntaje
        historico.puntaje_total = total_puntaje
        historico.puntaje_max = puntaje_maximo
        historico.tipo = "Ingreso"
        historico.clave = clave

        historico.save()
        foto.save()

        # ---------HISTORIAL---------------------------------
        pk = self.kwargs["pk"]
        preadmi = MILD_PreAdmision.objects.filter(pk=pk).first()
        base = MILD_Historial()
        base.fk_legajo_id = preadmi.fk_legajo.id
        base.fk_legajo_derivacion_id = preadmi.fk_derivacion_id
        base.fk_preadmi_id = preadmi.id
        base.movimiento = "MODIFICACION IVI"
        base.creado_por_id = self.request.user.id
        base.save()

        return redirect("MILD_indiceivi_ver", preadmi.id)


class MILDIndiceIviDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_1000D"
    template_name = "SIF_MILD/indiceivi_detail.html"
    model = MILD_PreAdmision

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        criterio = MILD_IndiceIVI.objects.filter(fk_preadmi_id=pk, tipo="Ingreso")
        object = MILD_PreAdmision.objects.filter(pk=pk).first()
        foto_ivi = MILD_Foto_IVI.objects.filter(
            fk_preadmi_id=pk, tipo="Ingreso"
        ).first()

        context["object"] = object
        context["foto_ivi"] = foto_ivi
        context["criterio"] = criterio
        context["puntaje"] = criterio.aggregate(total=Sum("fk_criterios_ivi__puntaje"))
        context["cantidad"] = criterio.count()
        context["modificables"] = criterio.filter(
            fk_criterios_ivi__modificable__iexact="SI"
        ).count()
        context["mod_puntaje"] = criterio.filter(
            fk_criterios_ivi__modificable__iexact="SI"
        ).aggregate(total=Sum("fk_criterios_ivi__puntaje"))
        context["ajustes"] = criterio.filter(fk_criterios_ivi__tipo="Ajustes").count()
        # context['maximo'] = foto_ivi.puntaje_max
        return context


class MILDPreAdmisiones2DetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_1000D"
    template_name = "SIF_MILD/preadmisiones_detail2.html"
    model = MILD_PreAdmision


class MILDPreAdmisiones3DetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_1000D"
    template_name = "SIF_MILD/preadmisiones_detail3.html"
    model = MILD_PreAdmision

    def get_context_data(self, **kwargs):
        pk = MILD_PreAdmision.objects.filter(pk=self.kwargs["pk"]).first()
        context = super().get_context_data(**kwargs)
        legajo = LegajosDerivaciones.objects.filter(pk=pk.fk_derivacion_id).first()
        familia = LegajoGrupoFamiliar.objects.filter(fk_legajo_2_id=legajo.fk_legajo_id)
        criterio = MILD_IndiceIVI.objects.filter(fk_preadmi_id=pk, tipo="Ingreso")
        criterio_ingreso = MILD_IndiceIngreso.objects.filter(
            fk_preadmi_id=pk, tipo="Ingreso"
        )
        foto_ivi = MILD_Foto_IVI.objects.filter(
            fk_preadmi_id=pk, tipo="Ingreso"
        ).first()
        foto_ingreso = MILD_Foto_Ingreso.objects.filter(
            fk_preadmi_id=pk, tipo="Ingreso"
        ).first()
        ivi = MILD_IndiceIVI.objects.filter(fk_legajo_id=legajo.fk_legajo_id)
        ingreso = MILD_IndiceIngreso.objects.filter(fk_legajo_id=legajo.fk_legajo_id)
        resultado = (
            ivi.values("clave", "creado", "programa")
            .annotate(total=Sum("fk_criterios_ivi__puntaje"))
            .order_by("-creado")
        )
        resultado_ingreso = (
            ingreso.values("clave", "creado", "programa")
            .annotate(total=Sum("fk_criterios_ingreso__puntaje"))
            .order_by("-creado")
        )

        context["ivi"] = ivi
        context["ingreso"] = ingreso
        context["legajo"] = legajo
        context["familia"] = familia
        context["foto_ivi"] = foto_ivi
        context["foto_ingreso"] = foto_ingreso
        if foto_ivi:
            context["puntaje"] = foto_ivi.puntaje
            context["puntaje_ingreso"] = foto_ingreso.puntaje
            context["maximo"] = foto_ivi.puntaje_max
        else:
            context["puntaje"] = 0
            context["puntaje_ingreso"] = 0
            context["maximo"] = 0
        if foto_ingreso:
            context["maximo_ingreso"] = foto_ingreso.puntaje_max
        else:
            context["maximo_ingreso"] = 0

        context["cantidad"] = criterio.count()
        context["cantidad_ingreso"] = criterio_ingreso.count()
        context["modificables"] = criterio.filter(
            fk_criterios_ivi__modificable__iexact="SI"
        ).count()
        context["mod_puntaje"] = criterio.filter(
            fk_criterios_ivi__modificable__iexact="SI"
        ).aggregate(total=Sum("fk_criterios_ivi__puntaje"))
        context["ajustes"] = criterio.filter(fk_criterios_ivi__tipo="Ajustes").count()
        context["resultado"] = resultado
        context["resultado_ingreso"] = resultado_ingreso
        context["legajo"] = legajo
        context["familia"] = familia
        context["criterios_total"] = criterio_ingreso.count()
        context["cant_sanitarios"] = criterio_ingreso.filter(
            fk_criterios_ingreso__tipo="Criterios sanitarios para el ingreso"
        ).count()
        context["cant_sociales"] = criterio_ingreso.filter(
            fk_criterios_ingreso__tipo="Criterios sociales para el ingreso"
        ).count()
        context["autonomos"] = criterio_ingreso.filter(
            fk_criterios_ingreso__tipo="Criteros autónomos de ingreso"
        ).all()
        return context

    def post(self, request, *args, **kwargs):
        if "admitir" in request.POST:
            preadmi = MILD_PreAdmision.objects.filter(pk=self.kwargs["pk"]).first()

            legajoMadre = LegajoGrupoFamiliar.objects.filter(
                fk_legajo_1_id=preadmi.fk_legajo_id, vinculo="Madre"
            ).first()
            alertaId = Alertas.objects.filter(
                nombre="Hijo en programa mil dias"
            ).first()
            print(legajoMadre)
            if legajoMadre is not None:
                validacionMadre = LegajoAlertas.objects.filter(
                    fk_legajo_id=legajoMadre.fk_legajo_2.id, fk_alerta_id=alertaId.id
                ).first()
                if validacionMadre is None:
                    legajosAlertasMadre = LegajoAlertas()
                    legajosAlertasMadre.fk_legajo_id = legajoMadre.fk_legajo_2.id
                    legajosAlertasMadre.creada_por_id = self.request.user.id
                    legajosAlertasMadre.fk_alerta_id = alertaId.id
                    legajosAlertasMadre.save()

            preadmi.admitido = "SI"
            preadmi.estado = "Admitido"
            preadmi.save()

            base1 = MILD_Admision()
            base1.fk_preadmi_id = preadmi.pk
            base1.creado_por_id = self.request.user.id
            base1.save()
            redirigir = base1.pk

            # ---------HISTORIAL---------------------------------
            pk = self.kwargs["pk"]
            legajo = MILD_PreAdmision.objects.filter(pk=pk).first()
            base = MILD_Historial()
            base.fk_legajo_id = legajo.fk_legajo.id
            base.fk_legajo_derivacion_id = legajo.fk_derivacion_id
            base.fk_preadmi_id = pk
            base.fk_admision_id = redirigir
            base.movimiento = "ADMITIDO"
            base.creado_por_id = self.request.user.id
            base.save()

            # Redirige de nuevo a la vista de detalle actualizada
            return redirect("MILD_asignado_admisiones_ver", redirigir)
        if "listaespera" in request.POST:
            # Realiza la actualización del campo aquí
            objeto = self.get_object()
            objeto.estado = "Lista de espera"
            objeto.save()

            # ---------HISTORIAL---------------------------------
            pk = self.kwargs["pk"]
            legajo = MILD_PreAdmision.objects.filter(pk=pk).first()
            base = MILD_Historial()
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
            legajo = MILD_PreAdmision.objects.filter(pk=pk).first()
            base = MILD_Historial()
            base.fk_legajo_id = legajo.fk_legajo.id
            base.fk_legajo_derivacion_id = legajo.fk_derivacion_id
            base.fk_preadmi_id = pk
            base.movimiento = "Rechazado"
            base.creado_por_id = self.request.user.id
            base.save()
            # Redirige de nuevo a la vista de detalle actualizada
            return HttpResponseRedirect(self.request.path_info)


class MILDAdmisionesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.programa_1000D"
    template_name = "SIF_MILD/adminsiones_list.html"
    model = MILD_Admision

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "1000D  Administrador",
            "1000D  Directivo",
            "1000D  Equipo operativo",
            "1000D  Equipo técnico",
            "1000D  Consultante",
            # "1000D  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa 1000D
        grupos_usuario = request.user.groups.filter(name__startswith="1000D")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        criterio = MILD_IndiceIVI.objects.all()
        criterio_ingreso = MILD_IndiceIngreso.objects.all()
        admi = MILD_Admision.objects.all()
        foto = MILD_Foto_IVI.objects.all()
        foto_ingreso = MILD_Foto_Ingreso.objects.all()
        conteo = MILD_IndiceIngreso.objects.values("fk_preadmi_id").annotate(
            total=Count("fk_preadmi_id")
        )

        context["conteo"] = conteo
        context["admi"] = admi
        context["foto"] = foto
        context["foto_ingreso"] = criterio_ingreso.aggregate(
            total=Count("fk_criterios_ingreso")
        )
        context["puntaje"] = criterio.aggregate(total=Sum("fk_criterios_ivi__puntaje"))
        context["puntaje_ingreso"] = criterio_ingreso.aggregate(
            total=Sum("fk_criterios_ingreso__puntaje")
        )
        return context


class MILDAdmisionesDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_1000D"
    model = MILD_Admision
    template_name = "SIF_MILD/admisiones_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = MILD_Admision.objects.filter(pk=self.kwargs["pk"]).first()
        preadmi = MILD_PreAdmision.objects.filter(pk=pk.fk_preadmi_id).first()
        criterio = MILD_IndiceIVI.objects.filter(fk_preadmi_id=preadmi, tipo="Ingreso")
        foto_ivi = MILD_Foto_IVI.objects.filter(
            fk_preadmi_id=preadmi, tipo="Ingreso"
        ).first()

        context["foto_ivi"] = foto_ivi
        context["puntaje"] = foto_ivi.puntaje
        context["cantidad"] = criterio.count()
        context["modificables"] = criterio.filter(
            fk_criterios_ivi__modificable__iexact="SI"
        ).count()
        context["mod_puntaje"] = criterio.filter(
            fk_criterios_ivi__modificable__iexact="SI"
        ).aggregate(total=Sum("fk_criterios_ivi__puntaje"))
        context["ajustes"] = criterio.filter(fk_criterios_ivi__tipo="Ajustes").count()
        context["maximo"] = foto_ivi.puntaje_max

        return context


class MILDAsignadoAdmisionDetail(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_1000D"
    template_name = "SIF_MILD/asignado_admisiones_detail.html"
    model = MILD_Admision

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        admi = MILD_Admision.objects.filter(pk=self.kwargs["pk"]).first()

        preadmi = MILD_PreAdmision.objects.filter(pk=admi.fk_preadmi_id).first()
        criterio = MILD_IndiceIVI.objects.filter(fk_preadmi_id=preadmi, tipo="Ingreso")
        criterio_ingreso = MILD_IndiceIngreso.objects.filter(
            fk_preadmi_id=preadmi, tipo="Ingreso"
        )
        criterio2 = MILD_IndiceIVI.objects.filter(fk_preadmi_id=preadmi, tipo="Ingreso")
        observaciones = MILD_Foto_IVI.objects.filter(
            fk_preadmi_id=preadmi, tipo="Ingreso"
        ).first()
        observaciones_ingreso = MILD_Foto_Ingreso.objects.filter(
            fk_preadmi_id=preadmi, tipo="Ingreso"
        ).first()
        observaciones2 = MILD_Foto_IVI.objects.filter(
            fk_preadmi_id=preadmi, tipo="Ingreso"
        ).first()
        intervenciones = MILD_Intervenciones.objects.filter(
            fk_admision_id=admi.id
        ).all()
        intervenciones_last = MILD_Intervenciones.objects.filter(
            fk_admision_id=admi.id
        ).last()
        foto_ivi_fin = MILD_Foto_IVI.objects.filter(
            fk_preadmi_id=admi.fk_preadmi_id, tipo="Ingreso"
        ).last()
        foto_ivi_inicio = MILD_Foto_IVI.objects.filter(
            fk_preadmi_id=admi.fk_preadmi_id, tipo="Ingreso"
        ).first()

        rol = obtener_rol(self.request)
        roles_inactivar = [
            "1000D  Administrador",
            "1000D  Directivo",
            "1000D  Equipo operativo",
            # "1000D  Equipo operativo",
            # "1000D  Consultante",
            # "1000D  Observador",
        ]
        if self.request.user.is_superuser or any(
            role in roles_inactivar for role in rol
        ):
            context["btn_inactivar"] = True
        else:
            context["btn_inactivar"] = False

        context["acompaniantes_tecnico"] = CHOICE_EQUIPO_TECNICO
        context["acompaniantes_asignado"] = CHOICE_ACOMPANANTES
        context["foto_ivi_fin"] = foto_ivi_fin
        context["foto_ivi_inicio"] = foto_ivi_inicio
        context["observaciones"] = observaciones
        context["observaciones_ingreso"] = observaciones_ingreso
        context["observaciones2"] = observaciones2
        context["criterio"] = criterio
        context["puntaje"] = criterio.aggregate(total=Sum("fk_criterios_ivi__puntaje"))
        context["cant_ingreso"] = criterio_ingreso.count()
        context["puntaje2"] = criterio2.aggregate(
            total=Sum("fk_criterios_ivi__puntaje")
        )
        context["object"] = admi
        context["vo"] = self.object
        context["intervenciones_count"] = intervenciones.count()
        context["intervenciones_last"] = intervenciones_last
        context["preadmi"] = preadmi

        return context

    def post(self, request, *args, **kwargs):
        if "acompaniante_asignado" in request.POST:
            admi = MILD_Admision.objects.filter(pk=self.kwargs["pk"]).first()
            preadmi = MILD_PreAdmision.objects.filter(pk=admi.fk_preadmi_id).first()
            if preadmi:
                nuevo_acompaniante = request.POST.get("acompaniante_asignado")
                preadmi.acompaniante_asignado = nuevo_acompaniante
                preadmi.save()

        return HttpResponseRedirect(self.request.path_info)


class MILDInactivaAdmisionDetail(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_1000D"
    template_name = "SIF_MILD/inactiva_admisiones_detail.html"
    model = MILD_Admision

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        admi = MILD_Admision.objects.filter(pk=self.kwargs["pk"]).first()

        preadmi = MILD_PreAdmision.objects.filter(pk=admi.fk_preadmi_id).first()
        criterio = MILD_IndiceIVI.objects.filter(fk_preadmi_id=preadmi, tipo="Egreso")
        intervenciones = MILD_Intervenciones.objects.filter(
            fk_admision_id=admi.id
        ).all()
        intervenciones_last = MILD_Intervenciones.objects.filter(
            fk_admision_id=admi.id
        ).last()
        foto_ivi_fin = MILD_Foto_IVI.objects.filter(
            fk_preadmi_id=admi.fk_preadmi_id, tipo="Egreso"
        ).first()
        foto_ivi_inicio = MILD_Foto_IVI.objects.filter(
            fk_preadmi_id=admi.fk_preadmi_id, tipo="Ingreso"
        ).first()

        context["foto_ivi_fin"] = foto_ivi_fin
        context["foto_ivi_inicio"] = foto_ivi_inicio
        context["criterio"] = criterio
        context["object"] = admi
        context["vo"] = self.object
        context["intervenciones_count"] = intervenciones.count()
        context["intervenciones_last"] = intervenciones_last

        return context


class MILDIntervencionesCreateView(PermisosMixin, CreateView):
    permission_required = "Usuarios.programa_1000D"
    model = MILD_Intervenciones  # Debería ser el modelo MILD_Intervenciones
    template_name = "SIF_MILD/intervenciones_form.html"
    form_class = MILD_IntervencionesForm

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "1000D  Administrador",
            "1000D  Directivo",
            "1000D  Equipo operativo",
            "1000D  Equipo técnico",
            # "1000D  Consultante",
            # "1000D  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa 1000D
        grupos_usuario = request.user.groups.filter(name__startswith="1000D")

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
        legajo = MILD_Admision.objects.filter(pk=pk).first()
        base = MILD_Historial()
        base.fk_legajo_id = legajo.fk_preadmi.fk_legajo.id
        base.fk_legajo_derivacion_id = legajo.fk_preadmi.fk_derivacion_id
        base.fk_preadmi_id = legajo.fk_preadmi.pk
        base.fk_admision_id = legajo.id  # Cambia a self.object.id
        base.movimiento = "INTERVENCION CREADA"
        base.creado_por_id = self.request.user.id
        base.save()

        return redirect("MILD_intervencion_ver", pk=self.object.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = MILD_Admision.objects.get(
            pk=self.kwargs["pk"]
        )  # Obtén el objeto directamente
        context["form"] = self.get_form()  # Obtiene una instancia del formulario

        return context


class MILDIntervencionesUpdateView(PermisosMixin, UpdateView):
    permission_required = "Usuarios.programa_1000D"
    model = MILD_Intervenciones
    template_name = "SIF_MILD/intervenciones_form.html"
    form_class = MILD_IntervencionesForm

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "1000D  Administrador",
            # "1000D  Directivo",
            # "1000D  Equipo operativo",
            # "1000D  Equipo técnico",
            # "1000D  Consultante",
            # "1000D  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa 1000D
        grupos_usuario = request.user.groups.filter(name__startswith="1000D")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def form_valid(self, form):
        pk = MILD_Intervenciones.objects.filter(pk=self.kwargs["pk"]).first()
        admi = MILD_Admision.objects.filter(id=pk.fk_admision.id).first()
        form.instance.fk_admision_id = admi.id
        form.instance.modificado_por_id = self.request.user.id
        self.object = form.save()

        # --------- HISTORIAL ---------------------------------
        pk = self.kwargs["pk"]
        pk = MILD_Intervenciones.objects.filter(pk=pk).first()
        legajo = MILD_Admision.objects.filter(pk=pk.fk_admision_id).first()
        base = MILD_Historial()
        base.fk_legajo_id = legajo.fk_preadmi.fk_legajo.id
        base.fk_legajo_derivacion_id = legajo.fk_preadmi.fk_derivacion_id
        base.fk_preadmi_id = legajo.fk_preadmi.pk
        base.fk_admision_id = legajo.pk
        base.movimiento = "INTERVENCION MODIFICADA"
        base.creado_por_id = self.request.user.id
        base.save()

        return redirect("MILD_intervencion_ver", self.object.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = MILD_Intervenciones.objects.filter(pk=self.kwargs["pk"]).first()
        admi = MILD_Admision.objects.filter(id=pk.fk_admision.id).first()

        context["object"] = admi

        return context


class MILDIntervencionesLegajosListView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_1000D"
    template_name = "SIF_MILD/intervenciones_legajo_list.html"
    model = MILD_Admision

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "1000D  Administrador",
            "1000D  Directivo",
            "1000D  Equipo operativo",
            "1000D  Equipo técnico",
            "1000D  Consultante",
            # "1000D  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa 1000D
        grupos_usuario = request.user.groups.filter(name__startswith="1000D")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        admi = MILD_Admision.objects.filter(pk=self.kwargs["pk"]).first()
        intervenciones = MILD_Intervenciones.objects.filter(
            fk_admision_id=admi.id
        ).all()
        intervenciones_last = MILD_Intervenciones.objects.filter(
            fk_admision_id=admi.id
        ).last()
        preadmi = MILD_PreAdmision.objects.filter(pk=admi.fk_preadmi_id).first()
        criterio = MILD_IndiceIVI.objects.filter(fk_preadmi_id=preadmi, tipo="Ingreso")
        if criterio:
            observaciones = MILD_Foto_IVI.objects.filter(
                clave=criterio.first().clave, tipo="Ingreso"
            ).first()
            context["observaciones"] = observaciones
        criterio2 = MILD_IndiceIVI.objects.filter(fk_preadmi_id=preadmi, tipo="Ingreso")
        if criterio2:
            observaciones2 = MILD_Foto_IVI.objects.filter(
                clave=criterio2.last().clave, tipo="Ingreso"
            ).first()
            context["observaciones2"] = observaciones2

        context["object"] = admi
        context["intervenciones"] = intervenciones
        context["intervenciones_count"] = intervenciones.count()
        context["intervenciones_last"] = intervenciones_last
        context["puntaje"] = criterio.aggregate(total=Sum("fk_criterios_ivi__puntaje"))
        context["puntaje2"] = criterio2.aggregate(
            total=Sum("fk_criterios_ivi__puntaje")
        )

        return context


class MILDIntervencionesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.programa_1000D"
    template_name = "SIF_MILD/intervenciones_list.html"
    model = MILD_Intervenciones

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "1000D  Administrador",
            "1000D  Directivo",
            "1000D  Equipo operativo",
            "1000D  Equipo técnico",
            "1000D  Consultante",
            # "1000D  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa 1000D
        grupos_usuario = request.user.groups.filter(name__startswith="1000D")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        intervenciones = MILD_Intervenciones.objects.all()
        context["intervenciones"] = intervenciones
        return context


class MILDIntervencionesDetail(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_1000D"
    template_name = "SIF_MILD/intervencion_detail.html"
    model = MILD_Intervenciones


class MILDOpcionesResponsablesCreateView(PermisosMixin, CreateView):
    permission_required = "Usuarios.programa_1000D"
    template_name = "SIF_MILD/intervenciones_resposables.html"
    model = OpcionesResponsables
    form_class = MILD_OpcionesResponsablesForm

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse("MILD_OpcionesResponsables"))


class MILDIntervencionesDeleteView(PermisosMixin, DeleteView):
    permission_required = "Usuarios.programa_1000D"
    model = MILD_Intervenciones
    template_name = "SIF_MILD/intervenciones_confirm_delete.html"
    success_url = reverse_lazy("MILD_intervenciones_listar")

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "1000D  Administrador",
            # "1000D  Directivo",
            # "1000D  Equipo operativo",
            # "1000D  Equipo técnico",
            # "1000D  Consultante",
            # "1000D  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa 1000D
        grupos_usuario = request.user.groups.filter(name__startswith="1000D")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def form_valid(self, form):

        if self.request.user.id != self.object.creado_por.id:
            messages.error(
                self.request,
                "Solo el usuario que generó esta derivación puede eliminarla.",
            )

            return redirect("MILD_preadmisiones_ver", pk=int(self.object.id))

        else:
            self.object.delete()
            return redirect(self.success_url)


class MILDAdmisionesBuscarListView(PermisosMixin, TemplateView):
    permission_required = "Usuarios.programa_1000D"
    template_name = "SIF_MILD/admisiones_buscar.html"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de grupos autorizados que permiten el acceso
        grupos_autorizados = [
            "1000D  Administrador",
            "1000D  Directivo",
            "1000D  Equipo operativo",
            "1000D  Equipo técnico",
            "1000D  Consultante",
            # "1000D  Observador",
        ]

        # Obtener los grupos del usuario que pertenecen al programa 1000D
        grupos_usuario = request.user.groups.filter(name__startswith="1000D")

        # Verificar si el usuario pertenece a alguno de los grupos autorizados
        if any(grupo.name in grupos_autorizados for grupo in grupos_usuario):
            return super().dispatch(request, *args, **kwargs)

        # Si no pertenece a un grupo autorizado, denegar el acceso
        raise PermissionDenied()

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        object_list = MILD_PreAdmision.objects.none()
        mostrar_resultados = False
        mostrar_btn_resetear = False
        query = self.request.GET.get("busqueda")
        if query:
            object_list = (
                MILD_Admision.objects.filter(
                    Q(fk_preadmi__fk_legajo__apellido__iexact=query)
                    | Q(fk_preadmi__fk_legajo__documento__iexact=query),
                    fk_preadmi__fk_derivacion__fk_programa_id=settings.PROG_MILD,
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


class MILDIndiceIviEgresoCreateView(PermisosMixin, CreateView):
    permission_required = "Usuarios.programa_1000D"
    model = Legajos
    template_name = "SIF_MILD/indiceivi_form_egreso.html"
    form_class = MILD_IndiceIviForm
    success_url = reverse_lazy("legajos_listar")

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super().get_context_data(**kwargs)
        admi = MILD_Admision.objects.filter(pk=pk).first()
        object = Legajos.objects.filter(pk=admi.fk_preadmi.fk_legajo.id).first()
        criterio = Criterios_IVI.objects.all()
        context["object"] = object
        context["criterio"] = criterio
        context["form2"] = MILD_IndiceIviHistorialForm()
        context["admi"] = admi
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        admi = MILD_Admision.objects.filter(pk=pk).first()
        # Genera una clave única utilizando uuid4 (versión aleatoria)
        preadmi = MILD_PreAdmision.objects.filter(
            fk_legajo_id=admi.fk_preadmi.fk_legajo.id
        ).first()
        foto_ivi = MILD_Foto_IVI.objects.filter(fk_preadmi_id=preadmi.id).first()
        clave = foto_ivi.clave
        nombres_campos = request.POST.keys()
        puntaje_maximo = Criterios_IVI.objects.aggregate(total=Sum("puntaje"))["total"]
        total_puntaje = 0
        historico = HistorialLegajoIndices()
        for f in nombres_campos:
            if f.isdigit():
                criterio_ivi = Criterios_IVI.objects.filter(id=f).first()
                # Sumar el valor de f al total_puntaje
                total_puntaje += int(criterio_ivi.puntaje)
                base = MILD_IndiceIVI()
                base.fk_criterios_ivi_id = f
                base.fk_legajo_id = admi.fk_preadmi.fk_legajo.id
                base.fk_preadmi_id = preadmi.id
                base.tipo = "Egreso"
                base.presencia = True
                base.programa = "MILD"
                historico.programa = base.programa
                base.clave = clave
                base.save()

        # total_puntaje contiene la suma de los valores de F
        foto = MILD_Foto_IVI()
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
        base = MILD_Historial()
        base.fk_legajo_id = legajo.fk_legajo.id
        base.fk_legajo_derivacion_id = legajo.fk_derivacion_id
        base.fk_preadmi_id = legajo.id
        base.movimiento = "IVI EGRESO"
        base.creado_por_id = self.request.user.id
        base.save()

        return redirect("MILD_admisiones_listar")
