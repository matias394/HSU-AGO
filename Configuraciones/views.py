from django.contrib import messages
from django.forms import BaseForm
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.views.generic.edit import FormMixin
from Usuarios.mixins import PermisosMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import *
from .forms import *
from django.db.models import Q
from django.urls import reverse_lazy
from .utils import insertar_programas
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied


def obtener_rol(request):
    if request.user.is_authenticated:
        # Supongamos que este método retorna los roles del usuario
        return list(request.user.groups.values_list("name", flat=True))
    return []


# region ############################################################### Secretarías


class SecretariasListView(PermisosMixin, ListView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Secretarias

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    # Funcion de busqueda

    def get_queryset(self):
        query = self.request.GET.get("busqueda")

        if query:
            object_list = self.model.objects.filter(
                Q(nombre__icontains=query) | Q(observaciones__icontains=query)
            ).distinct()

        else:
            object_list = self.model.objects.all()

        return object_list


class SecretariasDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Secretarias

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class SecretariasDeleteView(PermisosMixin, SuccessMessageMixin, DeleteView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Secretarias
    success_url = reverse_lazy("secretarias_listar")
    success_message = "El registro fue eliminado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class SecretariasCreateView(PermisosMixin, SuccessMessageMixin, CreateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Secretarias
    form_class = SecretariasForm
    success_message = "%(nombre)s fue registrado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class SecretariasUpdateView(PermisosMixin, SuccessMessageMixin, UpdateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Secretarias
    form_class = SecretariasForm
    success_message = "%(nombre)s fue editado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


# endregion


# region ############################################################### Subsecretarías


class SubsecretariasListView(PermisosMixin, ListView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Subsecretarias

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    # Funcion de busqueda

    def get_queryset(self):
        query = self.request.GET.get("busqueda")

        if query:
            object_list = self.model.objects.filter(
                Q(nombre__icontains=query)
                | Q(fk_secretaria__nombre__icontains=query)
                | Q(observaciones__icontains=query)
            ).distinct()

        else:
            object_list = self.model.objects.all()

        return object_list


class SubsecretariasDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Subsecretarias

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class SubsecretariasDeleteView(PermisosMixin, SuccessMessageMixin, DeleteView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Subsecretarias
    success_url = reverse_lazy("secretarias_listar")
    success_message = "El registro fue eliminado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class SubsecretariasCreateView(PermisosMixin, SuccessMessageMixin, CreateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Subsecretarias
    form_class = SubsecretariasForm
    success_message = "%(nombre)s fue registrado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class SubsecretariasUpdateView(PermisosMixin, SuccessMessageMixin, UpdateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Subsecretarias
    form_class = SubsecretariasForm
    success_message = "%(nombre)s fue editado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


# endregion


# region ############################################################### Organismos


class OrganismosListView(PermisosMixin, ListView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Organismos

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    # Funcion de busqueda

    def get_queryset(self):
        query = self.request.GET.get("busqueda")

        if query:
            object_list = self.model.objects.filter(
                Q(nombre__icontains=query)
            ).distinct()

        else:
            object_list = self.model.objects.all()

        return object_list


class OrganismosDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Organismos

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        # El pk que pasas a la URL

        pk = self.kwargs.get("pk")
        context = super(OrganismosDetailView, self).get_context_data(**kwargs)
        context["referentes"] = AgentesExternos.objects.filter(fk_organismo=pk)

        return context


class OrganismosDeleteView(PermisosMixin, SuccessMessageMixin, DeleteView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Organismos
    success_url = reverse_lazy("organismos_listar")
    success_message = "El registro fue eliminado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class OrganismosCreateView(PermisosMixin, SuccessMessageMixin, CreateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Organismos
    form_class = OrganismosForm
    success_message = "%(nombre)s fue registrado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class OrganismosUpdateView(PermisosMixin, SuccessMessageMixin, UpdateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Organismos
    form_class = OrganismosForm
    success_message = "%(nombre)s fue editado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


# endregion


# region ############################################################### Programas


class ProgramasListView(PermisosMixin, ListView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Programas
    template_name = "programas_list.html"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    # Funcion de busqueda

    def get_queryset(self):
        query = self.request.GET.get("busqueda")

        if query:
            object_list = self.model.objects.filter(
                Q(nombre__icontains=query)
                | Q(fk_secretaria__nombre__icontains=query)
                | Q(observaciones__icontains=query)
            ).distinct()

        else:
            object_list = self.model.objects.all()

        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class ProgramasDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Programas

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class ProgramasDeleteView(PermisosMixin, SuccessMessageMixin, DeleteView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Programas
    success_url = reverse_lazy("programas_listar")
    success_message = "El registro fue eliminado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class ProgramasCreateView(PermisosMixin, SuccessMessageMixin, CreateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Programas
    form_class = ProgramasForm
    success_message = "%(nombre)s fue registrado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class ProgramasUpdateView(PermisosMixin, SuccessMessageMixin, UpdateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Programas
    form_class = ProgramasForm
    success_message = "%(nombre)s fue editado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


# endregion


# region ############################################################### PlanesSociales


class PlanesSocialesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.programa_Configuracion"
    model = PlanesSociales

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    # Funcion de busqueda

    def get_queryset(self):
        query = self.request.GET.get("busqueda")

        if query:
            object_list = self.model.objects.filter(
                Q(nombre__icontains=query)
                | Q(jurisdiccion__icontains=query)
                | Q(observaciones__icontains=query)
            ).distinct()

        else:
            object_list = self.model.objects.all()

        return object_list


class PlanesSocialesDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_Configuracion"
    model = PlanesSociales

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class PlanesSocialesDeleteView(PermisosMixin, SuccessMessageMixin, DeleteView):
    permission_required = "Usuarios.programa_Configuracion"
    model = PlanesSociales
    success_url = reverse_lazy("planes_sociales_listar")
    success_message = "El registro fue eliminado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class PlanesSocialesCreateView(PermisosMixin, SuccessMessageMixin, CreateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = PlanesSociales
    form_class = PlanesSocialesForm
    success_message = "%(nombre)s fue registrado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class PlanesSocialesUpdateView(PermisosMixin, SuccessMessageMixin, UpdateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = PlanesSociales
    form_class = PlanesSocialesForm
    success_message = "%(nombre)s fue editado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


# endregion


# region ############################################################### AgentesExternos


class AgentesExternosListView(PermisosMixin, ListView):
    permission_required = "Usuarios.programa_Configuracion"
    model = AgentesExternos

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    # Funcion de busqueda

    def get_queryset(self):
        query = self.request.GET.get("busqueda")

        if query:
            object_list = self.model.objects.filter(
                Q(nombre__icontains=query)
                | Q(apellido__icontains=query)
                | Q(fk_organismo__nombre__icontains=query)
                | Q(email__icontains=query)
            ).distinct()

        else:
            object_list = self.model.objects.all()

        return object_list


class AgentesExternosDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_Configuracion"
    model = AgentesExternos

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class AgentesExternosDeleteView(PermisosMixin, SuccessMessageMixin, DeleteView):
    permission_required = "Usuarios.programa_Configuracion"
    model = AgentesExternos
    success_url = reverse_lazy("agentesexternos_listar")
    success_message = "El registro fue eliminado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class AgentesExternosCreateView(PermisosMixin, SuccessMessageMixin, CreateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = AgentesExternos
    form_class = AgentesExternosForm
    success_message = "%(nombre)s fue registrado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        """

        Si la petición viene desde una organización, la asigna a la instancia como incial.

        """

        pk = self.kwargs.get("pk")
        initial = super().get_initial()
        if pk:
            initial["fk_organismo"] = pk
        return initial


class AgentesExternosUpdateView(PermisosMixin, SuccessMessageMixin, UpdateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = AgentesExternos
    form_class = AgentesExternosForm
    success_message = "%(nombre)s fue editado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


# endregion


# region ############################################################### GruposDestinatarios


class GruposDestinatariosListView(PermisosMixin, ListView):
    permission_required = "Usuarios.programa_Configuracion"
    model = GruposDestinatarios

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    # Funcion de busqueda

    def get_queryset(self):
        query = self.request.GET.get("busqueda")

        if query:
            object_list = self.model.objects.filter(
                Q(nombre__icontains=query)
                | Q(m2m_usuarios__usuario__icontains=query)
                | Q(m2m_agentesexternos__nombre__icontains=query)
                | Q(m2m_agentesexternos__apellido__icontains=query)
                | Q(observaciones__icontains=query)
            ).distinct()

        else:
            object_list = self.model.objects.all()

        return object_list


class GruposDestinatariosDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_Configuracion"
    model = GruposDestinatarios

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class GruposDestinatariosDeleteView(PermisosMixin, SuccessMessageMixin, DeleteView):
    permission_required = "Usuarios.programa_Configuracion"
    model = GruposDestinatarios
    success_url = reverse_lazy("gruposdestinatarios_listar")
    success_message = "El registro fue eliminado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class GruposDestinatariosCreateView(PermisosMixin, SuccessMessageMixin, CreateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = GruposDestinatarios
    form_class = GruposDestinatariosForm
    success_message = "%(nombre)s fue registrado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class GruposDestinatariosUpdateView(PermisosMixin, SuccessMessageMixin, UpdateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = GruposDestinatarios
    form_class = GruposDestinatariosForm
    success_message = "%(nombre)s fue editado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


# endregion


# region ############################################################### Categoría de Alertas


class CategoriaAlertasListView(PermisosMixin, ListView):
    permission_required = "Usuarios.programa_Configuracion"
    model = CategoriaAlertas

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    # Funcion de busqueda

    def get_queryset(self):
        query = self.request.GET.get("busqueda")

        if query:
            object_list = self.model.objects.filter(nombre__icontains=query)

        else:
            object_list = self.model.objects.all()

        return object_list


class CategoriaAlertasDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_Configuracion"
    model = CategoriaAlertas

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class CategoriaAlertasDeleteView(PermisosMixin, SuccessMessageMixin, DeleteView):
    permission_required = "Usuarios.programa_Configuracion"
    model = CategoriaAlertas
    success_url = reverse_lazy("categoriaalertas_listar")
    success_message = "El registro fue eliminado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class CategoriaAlertasCreateView(PermisosMixin, SuccessMessageMixin, CreateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = CategoriaAlertas
    form_class = CategoriaAlertasForm
    success_message = "%(nombre)s fue registrado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class CategoriaAlertasUpdateView(PermisosMixin, SuccessMessageMixin, UpdateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = CategoriaAlertas
    form_class = CategoriaAlertasForm
    success_message = "%(nombre)s fue editado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


# endregion

# region ############################################################### Alertas


class AlertasListView(PermisosMixin, ListView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Alertas

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    # Funcion de busqueda

    def get_queryset(self):
        query = self.request.GET.get("busqueda")

        if query:
            object_list = self.model.objects.filter(nombre__icontains=query)

        else:
            object_list = self.model.objects.all()

        return object_list


class AlertasDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Alertas

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class AlertasDeleteView(PermisosMixin, SuccessMessageMixin, DeleteView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Alertas
    success_url = reverse_lazy("alertas_listar")
    success_message = "El registro fue eliminado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class AlertasCreateView(PermisosMixin, SuccessMessageMixin, CreateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Alertas
    form_class = AlertasForm
    success_message = "%(nombre)s fue registrado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class AlertasUpdateView(PermisosMixin, SuccessMessageMixin, UpdateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Alertas
    form_class = AlertasForm
    success_message = "%(nombre)s fue editado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


# endregion


# region ############################################################### Equipos


class EquiposListView(PermisosMixin, ListView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Equipos

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    # Funcion de busqueda

    def get_queryset(self):
        query = self.request.GET.get("busqueda")

        if query:
            object_list = self.model.objects.filter(
                Q(nombre__icontains=query)
                | Q(fk_programa__nombre__icontains=query)
                | Q(observaciones__icontains=query)
            ).distinct()

        else:
            object_list = self.model.objects.all()

        return object_list


class EquiposDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Equipos

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class EquiposDeleteView(PermisosMixin, SuccessMessageMixin, DeleteView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Equipos
    success_url = reverse_lazy("equipos_listar")
    success_message = "El registro fue eliminado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class EquiposCreateView(PermisosMixin, SuccessMessageMixin, CreateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Equipos
    form_class = EquiposForm
    success_message = "%(nombre)s fue registrado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""

        print(form.cleaned_data)

        self.object = form.save()

        return super().form_valid(form)


class EquiposUpdateView(PermisosMixin, SuccessMessageMixin, UpdateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Equipos
    form_class = EquiposForm
    success_message = "%(nombre)s fue editado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""

        print(form.cleaned_data)

        self.object = form.save()

        return super().form_valid(form)


# endregion


# region ############################################################### Acciones


class AccionesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Acciones

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    # Funcion de busqueda

    def get_queryset(self):
        query = self.request.GET.get("busqueda")

        if query:
            object_list = self.model.objects.filter(
                Q(nombre__icontains=query) | Q(dimension__icontains=query)
            ).distinct()

        else:
            object_list = self.model.objects.all()

        return object_list


class AccionesDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Acciones

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class AccionesDeleteView(PermisosMixin, SuccessMessageMixin, DeleteView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Acciones
    success_url = reverse_lazy("acciones_listar")
    success_message = "El registro fue eliminado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class AccionesCreateView(PermisosMixin, SuccessMessageMixin, CreateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Acciones
    form_class = AccionesForm
    success_message = "%(nombre)s fue registrado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class AccionesUpdateView(PermisosMixin, SuccessMessageMixin, UpdateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Acciones
    form_class = AccionesForm
    success_message = "%(nombre)s fue editado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


# endregion


# region ############################################################### Criterios


class CriteriosListView(PermisosMixin, ListView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Criterios

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    # Funcion de busqueda

    def get_queryset(self):
        query = self.request.GET.get("busqueda")

        if query:
            object_list = self.model.objects.filter(
                Q(nombre__icontains=query)
                | Q(dimension__icontains=query)
                | Q(fk_sujeto__nombre__icontains=query)
                | Q(observaciones__icontains=query)
            ).distinct()

        else:
            object_list = self.model.objects.all()

        return object_list


class CriteriosDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Criterios

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class CriteriosDeleteView(PermisosMixin, SuccessMessageMixin, DeleteView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Criterios
    success_url = reverse_lazy("criterios_listar")
    success_message = "El registro fue eliminado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class CriteriosCreateView(PermisosMixin, SuccessMessageMixin, CreateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Criterios
    form_class = CriteriosForm
    success_message = "%(nombre)s fue registrado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class CriteriosUpdateView(PermisosMixin, SuccessMessageMixin, UpdateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Criterios
    form_class = CriteriosForm
    success_message = "%(nombre)s fue editado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


# endregion


# region ############################################################### Indices


class IndicesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Indices

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    # Funcion de busqueda

    def get_queryset(self):
        query = self.request.GET.get("busqueda")

        if query:
            object_list = self.model.objects.filter(
                Q(nombre__icontains=query)
                | Q(m2m_criterios__nombre__icontains=query)
                | Q(m2m_programas__nombre__icontains=query)
                | Q(observaciones__icontains=query)
            ).distinct()

        else:
            object_list = self.model.objects.all()

        return object_list


class IndicesDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Indices

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class IndicesDeleteView(PermisosMixin, SuccessMessageMixin, DeleteView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Indices
    success_url = reverse_lazy("indices_listar")
    success_message = "El registro fue eliminado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class IndiceInline:
    """

    De esta clase heredaran las clases create y update, para realizar validaciones.

    """

    form_class = IndicesForm
    model = Indices
    template_name = "Configuraciones/indices_form.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()

        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function

        # otherwise, just save.

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, "formset_{0}_valid".format(name), None)

            if formset_save_func is not None:
                formset_save_func(formset)

            else:
                formset.save()

        messages.success(self.request, ("Índice guardado con éxito."))

        return redirect("indices_listar")

    def formset_variants_valid(self, formset):
        """

        Hook for custom formset saving.Useful if you have multiple formsets

        """

        variants = formset.save(commit=False)

        # self.save_formset(formset, contact)

        # add this 2 lines, if you have can_delete=True parameter

        # set in inlineformset_factory func

        for obj in formset.deleted_objects:
            obj.delete()

        for variant in variants:
            variant.fk_indice = Indices.objects.get(id=self.object.id)

            variant.save()


def delete_variant(request, pk):
    try:
        variant = IndiceCriterios.objects.get(id=pk)

    except IndiceCriterios.DoesNotExist:
        messages.success(request, "No existe el criterio")

        return redirect("indices_listar")

    variant.delete()

    messages.success(request, "Criterio eliminado con éxito")

    return redirect("indices_editar", pk=variant.fk_indice.id)


class IndicesCreateView(PermisosMixin, IndiceInline, CreateView):
    permission_required = "Usuarios.programa_Configuracion"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(IndicesCreateView, self).get_context_data(**kwargs)

        ctx["named_formsets"] = self.get_named_formsets()

        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                "variants": IndicesFormset(prefix="variants"),
            }

        else:
            return {
                "variants": IndicesFormset(
                    self.request.POST or None,
                    self.request.FILES or None,
                    prefix="variants",
                ),
            }


class IndicesUpdateView(PermisosMixin, IndiceInline, UpdateView):
    permission_required = "Usuarios.programa_Configuracion"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(IndicesUpdateView, self).get_context_data(**kwargs)

        ctx["named_formsets"] = self.get_named_formsets()

        return ctx

    def get_named_formsets(self):
        return {
            "variants": IndicesFormset(
                self.request.POST or None,
                self.request.FILES or None,
                instance=self.object,
                prefix="variants",
            ),
        }


# endregion


# region ############################################################### Vacantes


class VacantesListView(PermisosMixin, ListView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Vacantes

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        query = self.request.GET.get("busqueda")

        if query:
            object_list = self.model.objects.filter(
                Q(nombre__icontains=query)
                | Q(sala__icontains=query)
                | Q(turno__icontains=query)
            ).distinct()
        else:
            object_list = self.model.objects.all()

        return object_list


class VacantesDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Vacantes

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lista_cupos"] = CupoVacante.objects.filter(
            fk_vacante_id=self.kwargs["pk"]
        ).all()
        return context


class VacantesDeleteView(PermisosMixin, SuccessMessageMixin, DeleteView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Vacantes
    success_url = reverse_lazy("vacantes_listar")
    success_message = "El registro fue eliminado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class VacantesCreateView(PermisosMixin, SuccessMessageMixin, CreateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Vacantes
    form_class = VacantesForm
    success_message = "%(nombre)s fue registrado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cupoform"] = CupoVacantesForm()
        return context


class VacantesUpdateView(PermisosMixin, SuccessMessageMixin, UpdateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = Vacantes
    form_class = VacantesForm
    success_message = "%(nombre)s fue editado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cupoform"] = CupoVacantesForm()
        context["lista_cupos"] = CupoVacante.objects.filter(
            fk_vacante_id=self.kwargs["pk"]
        ).all()
        return context

    def post(self, request, *args, **kwargs):

        # Post del formulario de Cupo
        if "crear_cupo" in request.POST:
            nuevo_cupo = CupoVacante()
            nuevo_cupo.nombre = request.POST.get("nombre")
            nuevo_cupo.cupo = request.POST.get("cupo")
            nuevo_cupo.observaciones = request.POST.get("observaciones")
            nuevo_cupo.fk_vacante = self.get_object()
            nuevo_cupo.save()

        # Post de la vacante
        elif "vacante_actualizar" in request.POST:
            vacante = self.get_object()
            for clave, valor in request.POST.items():
                setattr(vacante, clave if not "fk_" in clave else f"{clave}_id", valor)
            vacante.save()

        url = reverse("vacantes_ver", args=[self.kwargs["pk"]])
        return HttpResponseRedirect(url)


# region ############################################################### Servicio Local Equipos


class SLEquiposListView(PermisosMixin, ListView):
    permission_required = "Usuarios.programa_Configuracion"
    model = SL_Equipos

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    # Funcion de busqueda

    def get_queryset(self):
        query = self.request.GET.get("busqueda")

        if query:
            object_list = self.model.objects.filter(
                Q(nombre__icontains=query) | Q(observaciones__icontains=query)
            ).distinct()

        else:
            object_list = self.model.objects.all()

        return object_list


class SLEquiposDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_Configuracion"
    model = SL_Equipos

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            # "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class SLEquiposDeleteView(PermisosMixin, SuccessMessageMixin, DeleteView):
    permission_required = "Usuarios.programa_Configuracion"
    model = SL_Equipos
    success_url = reverse_lazy("slequipos_listar")
    success_message = "El registro fue eliminado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class SLEquiposCreateView(PermisosMixin, SuccessMessageMixin, CreateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = SL_Equipos
    form_class = SL_Equipos_Form
    success_message = "%(nombre)s fue registrado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class SLEquiposUpdateView(PermisosMixin, SuccessMessageMixin, UpdateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = SL_Equipos
    form_class = SL_Equipos_Form
    success_message = "%(nombre)s fue editado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class SLIndicesVulnerabilidadListView(PermisosMixin, ListView):
    permission_required = "Usuarios.programa_Configuracion"
    model = SL_IndicesVulnerabilidad

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    # Funcion de busqueda

    def get_queryset(self):
        query = self.request.GET.get("busqueda")

        if query:
            object_list = self.model.objects.filter(
                Q(nombre__icontains=query) | Q(observaciones__icontains=query)
            ).distinct()

        else:
            object_list = self.model.objects.all()

        return object_list


class SLIndicesVulnerabilidadDetailView(PermisosMixin, DetailView):
    permission_required = "Usuarios.programa_Configuracion"
    model = SL_IndicesVulnerabilidad

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            # "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class SLIndicesVulnerabilidadDeleteView(PermisosMixin, SuccessMessageMixin, DeleteView):
    permission_required = "Usuarios.programa_Configuracion"
    model = SL_IndicesVulnerabilidad
    success_url = reverse_lazy("slindicesvulnerabilidad_list")
    success_message = "El registro fue eliminado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class SLIndicesVulnerabilidadCreateView(PermisosMixin, SuccessMessageMixin, CreateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = SL_IndicesVulnerabilidad
    form_class = SL_IndicesVulnerabilidadForm
    success_message = "%(nombre)s fue registrado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class SLIndicesVulnerabilidadUpdateView(PermisosMixin, SuccessMessageMixin, UpdateView):
    permission_required = "Usuarios.programa_Configuracion"
    model = SL_IndicesVulnerabilidad
    form_class = SL_IndicesVulnerabilidadForm
    success_message = "%(nombre)s fue editado correctamente"

    def dispatch(self, request, *args, **kwargs):
        # Permitir que los superusuarios siempre tengan acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Lista de permisos que no pueden entrar a la pagina
        permisos_a_verificar = [
            "Configuración  Directivo",
            "Configuración  Equipo operativo",
            "Configuración  Equipo técnico",
            "Configuración  Consultante",
            "Configuración  Observador",
        ]

        # Verifica si el usuario tiene alguno de estos permisos
        if not request.user.has_perm("Usuarios.programa_Configuracion"):
            raise PermissionDenied()
        if any(
            request.user.groups.filter(name=grupo).exists()
            for grupo in permisos_a_verificar
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


# endregion
