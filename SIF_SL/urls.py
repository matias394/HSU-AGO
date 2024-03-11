from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    # Derivaciones
    path('SL/derivaciones/listar', login_required(SLDerivacionesListView.as_view()), name='SL_derivaciones_listar'),
    path('SL/derivaciones/buscar', login_required(SLDerivacionesBuscarListView.as_view()), name='SL_derivaciones_buscar'),
    path('SL/derivaciones/ver/<pk>', login_required(SLDerivacionesDetailView.as_view()), name='SL_derivaciones_ver'),
    path('SL/derivaciones/editar/<pk>', login_required(SLDerivacionesUpdateView.as_view()), name='SL_derivaciones_editar'),
    path('SL/derivaciones/rechazo/<pk>', login_required(SLDerivacionesRechazo.as_view()), name='SL_derivaciones_rechazo'),
    # PreAdmisiones
    path('SL/preadmisiones/crear/<pk>', login_required(SLPreAdmisionesCreateView.as_view()), name='SL_preadmisiones_crear'),
    #path('SL/preadmisiones/referentes/<pk>', login_required(SLPreAdmisionesReferentesCreateView.as_view()), name='SL_preadmisiones_referentes_crear'),
    path('SL/preadmisiones/editar/<pk>', login_required(SLPreAdmisionesUpdateView.as_view()), name='SL_preadmisiones_editar'),
    path('SL/preadmisiones/ver/<pk>', login_required(SLPreAdmisionesDetailView.as_view()), name='SL_preadmisiones_ver'),
    path('SL/preadmisiones/ver3/<pk>', login_required(SLPreAdmisiones3DetailView.as_view()), name='SL_preadmisiones_ver3'),
    path('SL/preadmisiones/listar', login_required(SLPreAdmisionesListView.as_view()), name='SL_preadmisiones_listar'),
    path('SL/preadmisiones/buscar', login_required(SLPreAdmisionesBuscarListView.as_view()), name='SL_preadmisiones_buscar'),
    path('SL/preadmisiones/eliminar/<pk>', login_required(SLPreAdmisionesDeleteView.as_view()), name='SL_preadmisiones_eliminar'),

    # Preadmisiones Archivos
    path('SL/preadmisiones/archivos/listar/<pk>', login_required(PreAdmArchivosListView.as_view()), name='preadmarchivos_listar'),
    path('SL/preadmisiones/archivos/crear/<pk>', login_required(PreAdmArchivosCreateView.as_view()), name='preadmarchivos_crear'),
    path('SL/preadmisiones/archivos/crear/ajax/', login_required(PreAdmCreateArchivo.as_view()), name='preadmarchivo_ajax_crear'),    
    path('SL/preadmisiones/archivos/borrar/ajax/', login_required(PreAdmDeleteArchivo.as_view()), name='preadmarchivo_ajax_borrar'),
    
    # Indice Ingreso
    path('SL/criterios_ingreso/crear', login_required(SLCriteriosIngresoCreateView.as_view()), name='SL_criterios_ingreso_crear'),
    path('SL/indice_ingreso/crear/<pk>', login_required(SLIndiceIngresoCreateView.as_view()), name='SL_indiceingreso_crear'),
    #path('SL/indice_ivi_egreso/crear/<pk>', login_required(SLIndiceIviEgresoCreateView.as_view()), name='SL_indiceiviegreso_crear'),
    path('SL/indice_ingreso/ver/<pk>', login_required(SLIndiceIngresoDetailView.as_view()), name='SL_indiceingreso_ver'),
    path('SL/indice_ingreso/editar/<pk>', login_required(SLIndiceIngresoUpdateView.as_view()), name='SL_indiceingreso_editar'),
    # IVI
    path('SL/criterios_ivi/crear', login_required(SLCriteriosIVICreateView.as_view()), name='SL_criterios_ivi_crear'),
    path('SL/indice_ivi/crear/<pk>', login_required(SLIndiceIviCreateView.as_view()), name='SL_indiceivi_crear'),
    path('SL/indice_ivi_egreso/crear/<pk>', login_required(SLIndiceIviEgresoCreateView.as_view()), name='SL_indiceiviegreso_crear'),
    path('SL/indice_ivi/ver/<pk>', login_required(SLIndiceIviDetailView.as_view()), name='SL_indiceivi_ver'),
    path('SL/indice_ivi/editar/<pk>', login_required(SLIndiceIviUpdateView.as_view()), name='SL_indiceivi_editar'),
    # Admisiones
    path('SL/admisiones/ver/<pk>', login_required(SLAdmisionesDetailView.as_view()), name='SL_admisiones_ver'),
    path('SL/admisiones/listar/', login_required(SLAdmisionesListView.as_view()), name='SL_admisiones_listar'),
    path('SL/admisiones/buscar', login_required(SLAdmisionesBuscarListView.as_view()), name='SL_admisiones_buscar'),
    path('SL/asignado_admisiones/ver/<pk>', login_required(SLAsignadoAdmisionDetail.as_view()), name='SL_asignado_admisiones_ver'),
    path('SL/inactiva_admisiones/ver/<pk>', login_required(SLInactivaAdmisionDetail.as_view()), name='SL_inactiva_admisiones_ver'),
    # Intervensiones
    path('SL/intervenciones/crear/<pk>', login_required(SLIntervencionesCreateView.as_view()), name='SL_intervenciones_crear'),
    path('SL/intervenciones/ver/<pk>', login_required(SLIntervencionesLegajosListView.as_view()), name='SL_intervenciones_legajos_listar'),
    path('SL/intervenciones/listar/', login_required(SLIntervencionesListView.as_view()), name='SL_intervenciones_listar'),
    path('SL/intervencion/ver/<pk>', login_required(SLIntervencionesDetail.as_view()), name='SL_intervencion_ver'),
    path('SL/intervenciones/editar/<pk>', login_required(SLIntervencionesUpdateView.as_view()), name='SL_intervencion_editar'),
    path('SL/intervenciones/borrar/<pk>', login_required(SLIntervencionesDeleteView.as_view()), name='SL_intervencion_borrar'),

    ]

