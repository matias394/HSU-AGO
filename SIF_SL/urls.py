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
    path('SL/preadmisiones/editar/<pk>', login_required(SLPreAdmisionesUpdateView.as_view()), name='SL_preadmisiones_editar'),
    path('SL/preadmisiones/ver/<pk>', login_required(SLPreAdmisionesDetailView.as_view()), name='SL_preadmisiones_ver'),
    #path('SL/preadmisiones/ver3/<pk>', login_required(SLPreAdmisiones3DetailView.as_view()), name='SL_preadmisiones_ver3'),
    path('SL/preadmisiones/listar', login_required(SLPreAdmisionesListView.as_view()), name='SL_preadmisiones_listar'),
    path('SL/preadmisiones/buscar', login_required(SLPreAdmisionesBuscarListView.as_view()), name='SL_preadmisiones_buscar'),
    path('SL/preadmisiones/eliminar/<pk>', login_required(SLPreAdmisionesDeleteView.as_view()), name='SL_preadmisiones_eliminar'),
    # Designar Equipo
    path('SL/designarequipo/crear/<pk>', login_required(SLDesignarEquipoCreateView.as_view()), name='SL_designarequipo_crear'),
    path('SL/designarequipo/editar/<pk>', login_required(SLDesignarEquipoUpdateView.as_view()), name='SL_designarequipo_editar'),
    
    # Indice Vulneracion
    path('SL/indice_vulneracion/crear/<pk>', login_required(SLIndiceVulneracionCreateView.as_view()), name='SL_indicevulneracion_crear'),
    #path('SL/indice_vulneracion/ver/<pk>', login_required(SLIndiceVulneracionDetailView.as_view()), name='SL_indicevulneracion_ver'),
    path('SL/indice_vulneracion/editar/<pk>/', login_required(SLIndiceVulneracionUpdateView.as_view()), name='SL_indicevulneracion_editar'),

    # Admisiones
    path('SL/admisiones/ver/<pk>', login_required(SLAdmisionesDetailView.as_view()), name='SL_admisiones_ver'),
    path('SL/admisiones/listar/', login_required(SLAdmisionesListView.as_view()), name='SL_admisiones_listar'),
    #path('SL/admisiones/buscar', login_required(SLAdmisionesBuscarListView.as_view()), name='SL_admisiones_buscar'),
    #path('SL/asignado_admisiones/ver/<pk>', login_required(SLAsignadoAdmisionDetail.as_view()), name='SL_asignado_admisiones_ver'),
    #path('SL/inactiva_admisiones/ver/<pk>', login_required(SLInactivaAdmisionDetail.as_view()), name='SL_inactiva_admisiones_ver'),
    # Intervensiones
    path('SL/intervenciones/crear/<pk>', login_required(SLIntervencionesCreateView.as_view()), name='SL_intervenciones_crear'),
    #path('SL/intervenciones/ver/<pk>', login_required(SLIntervencionesLegajosListView.as_view()), name='SL_intervenciones_legajos_listar'),
    path('SL/intervenciones/listar/', login_required(SLIntervencionesListView.as_view()), name='SL_intervenciones_listar'),
    path('SL/intervencion/ver/<pk>', login_required(SLIntervencionesDetail.as_view()), name='SL_intervencion_ver'),
    path('SL/intervenciones/editar/<pk>', login_required(SLIntervencionesUpdateView.as_view()), name='SL_intervencion_editar'),
    path('SL/intervenciones/borrar/<pk>', login_required(SLIntervencionesDeleteView.as_view()), name='SL_intervencion_borrar'),

    path('SL/equipos/ver/<pk>', login_required(SL_EquiposDesignadosDetailView.as_view()), name='sl_equipodesignado_ver'),
    path('SL/equipos/listar/', login_required(SL_EquiposDesignadosListView.as_view()), name='sl_equipodesignado_list'),
    ]

