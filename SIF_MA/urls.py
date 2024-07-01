from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    # Derivaciones
    path('MA/derivaciones/listar', login_required(MADerivacionesListView.as_view()), name='MA_derivaciones_listar'),
    path('MA/derivaciones/buscar', login_required(MADerivacionesBuscarListView.as_view()), name='MA_derivaciones_buscar'),
    path('MA/derivaciones/ver/<pk>', login_required(MADerivacionesDetailView.as_view()), name='MA_derivaciones_ver'),
    path('MA/derivaciones/editar/<pk>', login_required(MADerivacionesUpdateView.as_view()), name='MA_derivaciones_editar'),
    path('MA/derivaciones/rechazo/<pk>', login_required(MADerivacionesRechazo.as_view()), name='MA_derivaciones_rechazo'),
    # PreAdmisiones
    path('MA/preadmisiones/crear/<pk>', login_required(MAPreAdmisionesCreateView.as_view()), name='MA_preadmisiones_crear'),
    path('MA/preadmisiones/editar/<pk>', login_required(MAPreAdmisionesUpdateView.as_view()), name='MA_preadmisiones_editar'),
    path('MA/preadmisiones/ver/<pk>', login_required(MAPreAdmisionesDetailView.as_view()), name='MA_preadmisiones_ver'),
    path('MA/preadmisiones/listar', login_required(MAPreAdmisionesListView.as_view()), name='MA_preadmisiones_listar'),
    path('MA/preadmisiones/buscar', login_required(MAPreAdmisionesBuscarListView.as_view()), name='MA_preadmisiones_buscar'),
    path('MA/preadmisiones/eliminar/<pk>', login_required(MAPreAdmisionesDeleteView.as_view()), name='MA_preadmisiones_eliminar'),
    # Admisiones
    path('MA/admisiones/ver/<pk>', login_required(MAAdmisionesDetailView.as_view()), name='MA_admisiones_ver'),
    path('MA/admisiones/crear/<pk>', login_required(MAAdmisionesCreateView.as_view()), name='MA_admisiones_crear'),
    path('MA/admisiones/editar/<pk>', login_required(MAAdmisionesUpdateView.as_view()), name='MA_admisiones_editar'),
    path('MA/admisiones/listar/', login_required(MAAdmisionesListView.as_view()), name='MA_admisiones_listar'),
    path('MA/admisiones/buscar', login_required(MAAdmisionesBuscarListView.as_view()), name='MA_admisiones_buscar'),
    path('MA/asignado_admisiones/ver/<pk>', login_required(MAAsignadoAdmisionDetail.as_view()), name='MA_asignado_admisiones_ver'),
    path('MA/inactiva_admisiones/ver/<pk>', login_required(MAInactivaAdmisionDetail.as_view()), name='MA_inactiva_admisiones_ver'),
    # Intervensiones
    path('MA/intervenciones/crear/<pk>', login_required(MAIntervencionesCreateView.as_view()), name='MA_intervenciones_crear'),
    path('MA/intervenciones/ver/<pk>', login_required(MAIntervencionesLegajosListView.as_view()), name='MA_intervenciones_legajos_listar'),
    path('MA/intervenciones/listar/', login_required(MAIntervencionesListView.as_view()), name='MA_intervenciones_listar'),
    path('MA/intervencion/ver/<pk>', login_required(MAIntervencionesDetail.as_view()), name='MA_intervencion_ver'),
    path('MA/intervenciones/editar/<pk>', login_required(MAIntervencionesUpdateView.as_view()), name='MA_intervencion_editar'),
    path('MA/intervenciones/borrar/<pk>', login_required(MAIntervencionesDeleteView.as_view()), name='MA_intervencion_borrar'),

    path('MA/expediente/ver/<pk>', login_required(MA_ExpedienteDetailView.as_view()), name='MA_expediente_ver'),
    path('MA/expediente/listar/', login_required(MA_ExpedienteListView.as_view()), name='MA_expediente_listar'),

    ]

