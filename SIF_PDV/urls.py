from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    # Derivaciones
    path('PDV/derivaciones/listar', login_required(PDVDerivacionesListView.as_view()), name='PDV_derivaciones_listar'),
    path('PDV/derivaciones/buscar', login_required(PDVDerivacionesBuscarListView.as_view()), name='PDV_derivaciones_buscar'),
    path('PDV/derivaciones/ver/<pk>', login_required(PDVDerivacionesDetailView.as_view()), name='PDV_derivaciones_ver'),
    path('PDV/derivaciones/rechazo/<pk>', login_required(PDVDerivacionesRechazo.as_view()), name='PDV_derivaciones_rechazo'),
    # PreAdmisiones
    path('PDV/preadmisiones/crear/<pk>', login_required(PDVPreAdmisionesCreateView.as_view()), name='PDV_preadmisiones_crear'),
    path('PDV/preadmisiones/editar/<pk>', login_required(PDVPreAdmisionesUpdateView.as_view()), name='PDV_preadmisiones_editar'),
    path('PDV/preadmisiones/ver/<pk>', login_required(PDVPreAdmisionesDetailView.as_view()), name='PDV_preadmisiones_ver'),
    path('PDV/preadmisiones/ver3/<pk>', login_required(PDVPreAdmisiones3DetailView.as_view()), name='PDV_preadmisiones_ver3'),
    path('PDV/preadmisiones/listar', login_required(PDVPreAdmisionesListView.as_view()), name='PDV_preadmisiones_listar'),
    path('PDV/preadmisiones/buscar', login_required(PDVPreAdmisionesBuscarListView.as_view()), name='PDV_preadmisiones_buscar'),
    path('PDV/preadmisiones/eliminar/<pk>', login_required(PDVPreAdmisionesDeleteView.as_view()), name='PDV_preadmisiones_eliminar'),
    # IVI
    path('PDV/criterios_ivi/crear', login_required(PDVCriteriosIVICreateView.as_view()), name='PDV_criterios_ivi_crear'),
    path('PDV/indice_ivi/crear/<pk>', login_required(PDVIndiceIviCreateView.as_view()), name='PDV_indiceivi_crear'),
    path('PDV/indice_ivi_egreso/crear/<pk>', login_required(PDVIndiceIviEgresoCreateView.as_view()), name='PDV_indiceiviegreso_crear'),
    path('PDV/indice_ivi/ver/<pk>', login_required(PDVIndiceIviDetailView.as_view()), name='PDV_indiceivi_ver'),
    path('PDV/indice_ivi/editar/<pk>', login_required(PDVIndiceIviUpdateView.as_view()), name='PDV_indiceivi_editar'),
    # Vacantes
    path('PDV/vacantes/list/', login_required(PDVVacantesListView.as_view()), name='PDV_vacantes_listar'),
    path('PDV/vacantes/ver/<pk>', login_required(PDVVacantesDetailView.as_view()), name='PDV_vacantes_ver'),
    path('PDV/vacantes/crear/<pk>', login_required(PDVVacantesAdmision.as_view()), name='PDV_vacantes_form'),
    path('PDV/vacantes/cambio/<pk>', login_required(PDVVacantesAdmisionCambio.as_view()), name='PDV_vacantes_form_cambio'),
    # Admisiones
    path('PDV/admisiones/ver/<pk>', login_required(PDVAdmisionesDetailView.as_view()), name='PDV_admisiones_ver'),
    path('PDV/admisiones/listar/', login_required(PDVAdmisionesListView.as_view()), name='PDV_admisiones_listar'),
    path('PDV/admisiones/buscar', login_required(PDVAdmisionesBuscarListView.as_view()), name='PDV_admisiones_buscar'),
    path('PDV/asignado_admisiones/ver/<pk>', login_required(PDVAsignadoAdmisionDetail.as_view()), name='PDV_asignado_admisiones_ver'),
    path('PDV/inactiva_admisiones/ver/<pk>', login_required(PDVInactivaAdmisionDetail.as_view()), name='PDV_inactiva_admisiones_ver'),
    # Intervensiones
    path('PDV/intervenciones/crear/<pk>', login_required(PDVIntervencionesCreateView.as_view()), name='PDV_intervenciones_crear'),
    path('PDV/intervenciones/ver/<pk>', login_required(PDVIntervencionesLegajosListView.as_view()), name='PDV_intervenciones_legajos_listar'),
    path('PDV/intervenciones/listar/', login_required(PDVIntervencionesListView.as_view()), name='PDV_intervenciones_listar'),
    path('PDV/intervencion/ver/<pk>', login_required(PDVIntervencionesDetail.as_view()), name='PDV_intervencion_ver'),
    path('PDV/intervenciones/editar/<pk>', login_required(PDVIntervencionesUpdateView.as_view()), name='PDV_intervencion_editar'),
    path('PDV/intervenciones/borrar/<pk>', login_required(PDVIntervencionesDeleteView.as_view()), name='PDV_intervencion_borrar'),

    ]

