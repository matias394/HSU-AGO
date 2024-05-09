from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    # Derivaciones
    path('UMI/derivaciones/listar', login_required(UMIDerivacionesListView.as_view()), name='UMI_derivaciones_listar'),
    path('UMI/derivaciones/buscar', login_required(UMIDerivacionesBuscarListView.as_view()), name='UMI_derivaciones_buscar'),
    path('UMI/derivaciones/ver/<pk>', login_required(UMIDerivacionesDetailView.as_view()), name='UMI_derivaciones_ver'),
    path('UMI/derivaciones/editar/<pk>', login_required(UMIDerivacionesUpdateView.as_view()), name='UMI_derivaciones_editar'),
    path('UMI/derivaciones/rechazo/<pk>', login_required(UMIDerivacionesRechazo.as_view()), name='UMI_derivaciones_rechazo'),
    # PreAdmisiones
    path('UMI/preadmisiones/crear/<pk>', login_required(UMIPreAdmisionesCreateView.as_view()), name='UMI_preadmisiones_crear'),
    path('UMI/preadmisiones/editar/<pk>', login_required(UMIPreAdmisionesUpdateView.as_view()), name='UMI_preadmisiones_editar'),
    path('UMI/preadmisiones/ver/<pk>', login_required(UMIPreAdmisionesDetailView.as_view()), name='UMI_preadmisiones_ver'),
    path('UMI/preadmisiones/ver2/<pk>', login_required(UMIPreAdmisiones2DetailView.as_view()), name='UMI_preadmisiones_ver2'),
    path('UMI/preadmisiones/ver3/<pk>', login_required(UMIPreAdmisiones3DetailView.as_view()), name='UMI_preadmisiones_ver3'),
    path('UMI/preadmisiones/listar', login_required(UMIPreAdmisionesListView.as_view()), name='UMI_preadmisiones_listar'),
    path('UMI/preadmisiones/buscar', login_required(UMIPreAdmisionesBuscarListView.as_view()), name='UMI_preadmisiones_buscar'),
    path('UMI/preadmisiones/eliminar/<pk>', login_required(UMIPreAdmisionesDeleteView.as_view()), name='UMI_preadmisiones_eliminar'),
    # Indice Ingreso
    path('UMI/criterios_ingreso/crear', login_required(UMICriteriosIngresoCreateView.as_view()), name='UMI_criterios_ingreso_crear'),
    path('UMI/indice_ingreso/crear/<pk>', login_required(UMIIndiceIngresoCreateView.as_view()), name='UMI_indiceingreso_crear'),
    #path('UMI/indice_ivi_egreso/crear/<pk>', login_required(UMIIndiceIviEgresoCreateView.as_view()), name='UMI_indiceiviegreso_crear'),
    path('UMI/indice_ingreso/ver/<pk>', login_required(UMIIndiceIngresoDetailView.as_view()), name='UMI_indiceingreso_ver'),
    path('UMI/indice_ingreso/editar/<pk>', login_required(UMIIndiceIngresoUpdateView.as_view()), name='UMI_indiceingreso_editar'),
    # IVI
    path('UMI/criterios_ivi/crear', login_required(UMICriteriosIVICreateView.as_view()), name='UMI_criterios_ivi_crear'),
    path('UMI/indice_ivi/crear/<pk>', login_required(UMIIndiceIviCreateView.as_view()), name='UMI_indiceivi_crear'),
    path('UMI/indice_ivi_egreso/crear/<pk>', login_required(UMIIndiceIviEgresoCreateView.as_view()), name='UMI_indiceiviegreso_crear'),
    path('UMI/indice_ivi/ver/<pk>', login_required(UMIIndiceIviDetailView.as_view()), name='UMI_indiceivi_ver'),
    path('UMI/indice_ivi/editar/<pk>', login_required(UMIIndiceIviUpdateView.as_view()), name='UMI_indiceivi_editar'),
    # Admisiones
    path('UMI/admisiones/ver/<pk>', login_required(UMIAdmisionesDetailView.as_view()), name='UMI_admisiones_ver'),
    path('UMI/admisiones/listar/', login_required(UMIAdmisionesListView.as_view()), name='UMI_admisiones_listar'),
    path('UMI/admisiones/buscar', login_required(UMIAdmisionesBuscarListView.as_view()), name='UMI_admisiones_buscar'),
    path('UMI/asignado_admisiones/ver/<pk>', login_required(UMIAsignadoAdmisionDetail.as_view()), name='UMI_asignado_admisiones_ver'),
    path('UMI/inactiva_admisiones/ver/<pk>', login_required(UMIInactivaAdmisionDetail.as_view()), name='UMI_inactiva_admisiones_ver'),
    # Intervensiones
    path('UMI/intervenciones/crear/<pk>', login_required(UMIIntervencionesCreateView.as_view()), name='UMI_intervenciones_crear'),
    path('UMI/intervenciones/ver/<pk>', login_required(UMIIntervencionesLegajosListView.as_view()), name='UMI_intervenciones_legajos_listar'),
    path('UMI/intervenciones/listar/', login_required(UMIIntervencionesListView.as_view()), name='UMI_intervenciones_listar'),
    path('UMI/intervencion/ver/<pk>', login_required(UMIIntervencionesDetail.as_view()), name='UMI_intervencion_ver'),
    path('UMI/intervenciones/editar/<pk>', login_required(UMIIntervencionesUpdateView.as_view()), name='UMI_intervencion_editar'),
    path('UMI/intervenciones/borrar/<pk>', login_required(UMIIntervencionesDeleteView.as_view()), name='UMI_intervencion_borrar'),

    ]

