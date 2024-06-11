from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    # Derivaciones
    path('DESCEN/derivaciones/listar', login_required(DESCENDerivacionesListView.as_view()), name='DESCEN_derivaciones_listar'),
    path('DESCEN/derivaciones/buscar', login_required(DESCENDerivacionesBuscarListView.as_view()), name='DESCEN_derivaciones_buscar'),
    path('DESCEN/derivaciones/ver/<pk>', login_required(DESCENDerivacionesDetailView.as_view()), name='DESCEN_derivaciones_ver'),
    path('DESCEN/derivaciones/editar/<pk>', login_required(DESCENDerivacionesUpdateView.as_view()), name='DESCEN_derivaciones_editar'),
    path('DESCEN/derivaciones/rechazo/<pk>', login_required(DESCENDerivacionesRechazo.as_view()), name='DESCEN_derivaciones_rechazo'),
    # PreAdmisiones
    path('DESCEN/preadmisiones/crear/<pk>', login_required(DESCENPreAdmisionesCreateView.as_view()), name='DESCEN_preadmisiones_crear'),
    path('DESCEN/preadmisiones/editar/<pk>', login_required(DESCENPreAdmisionesUpdateView.as_view()), name='DESCEN_preadmisiones_editar'),
    path('DESCEN/preadmisiones/ver/<pk>', login_required(DESCENPreAdmisionesDetailView.as_view()), name='DESCEN_preadmisiones_ver'),
    path('DESCEN/preadmisiones/ver2/<pk>', login_required(DESCENPreAdmisiones2DetailView.as_view()), name='DESCEN_preadmisiones_ver2'),
    path('DESCEN/preadmisiones/ver3/<pk>', login_required(DESCENPreAdmisiones3DetailView.as_view()), name='DESCEN_preadmisiones_ver3'),
    path('DESCEN/preadmisiones/listar', login_required(DESCENPreAdmisionesListView.as_view()), name='DESCEN_preadmisiones_listar'),
    path('DESCEN/preadmisiones/buscar', login_required(DESCENPreAdmisionesBuscarListView.as_view()), name='DESCEN_preadmisiones_buscar'),
    path('DESCEN/preadmisiones/eliminar/<pk>', login_required(DESCENPreAdmisionesDeleteView.as_view()), name='DESCEN_preadmisiones_eliminar'),
    # IVI
    path('DESCEN/criterios_ivi/crear', login_required(DESCENCriteriosIVICreateView.as_view()), name='DESCEN_criterios_ivi_crear'),
    path('DESCEN/indice_ivi/crear/<pk>', login_required(DESCENIndiceIviCreateView.as_view()), name='DESCEN_indiceivi_crear'),
    path('DESCEN/indice_ivi_egreso/crear/<pk>', login_required(DESCENIndiceIviEgresoCreateView.as_view()), name='DESCEN_indiceiviegreso_crear'),
    path('DESCEN/indice_ivi/ver/<pk>', login_required(DESCENIndiceIviDetailView.as_view()), name='DESCEN_indiceivi_ver'),
    path('DESCEN/indice_ivi/editar/<pk>', login_required(DESCENIndiceIviUpdateView.as_view()), name='DESCEN_indiceivi_editar'),
    # Vacantes
    path('DESCEN/vacantes/list/', login_required(DESCENVacantesListView.as_view()), name='DESCEN_vacantes_listar'),
    path('DESCEN/vacantes/ver/<pk>', login_required(DESCENVacantesDetailView.as_view()), name='DESCEN_vacantes_ver'),
    path('DESCEN/vacantes/crear/<pk>', login_required(DESCENVacantesAdmision.as_view()), name='DESCEN_vacantes_form'),
    path('DESCEN/vacantes/cambio/<pk>', login_required(DESCENVacantesAdmisionCambio.as_view()), name='DESCEN_vacantes_form_cambio'),
    path('DESCEN/vacantes/stock/list/<pk>', login_required(DESCENVacantesStockListView.as_view()), name='DESCEN_vacantes_stock_listar'),
    path('DESCEN/vacantes/stock/edit/<pk>', login_required(DESCENVacantesStockEditView.as_view()), name='DESCEN_vacantes_stock_edit'),
    # Admisiones
    path('DESCEN/admisiones/ver/<pk>', login_required(DESCENAdmisionesDetailView.as_view()), name='DESCEN_admisiones_ver'),
    path('DESCEN/admisiones/listar/', login_required(DESCENAdmisionesListView.as_view()), name='DESCEN_admisiones_listar'),
    path('DESCEN/admisiones/buscar', login_required(DESCENAdmisionesBuscarListView.as_view()), name='DESCEN_admisiones_buscar'),
    path('DESCEN/asignado_admisiones/ver/<pk>', login_required(DESCENAsignadoAdmisionDetail.as_view()), name='DESCEN_asignado_admisiones_ver'),
    path('DESCEN/inactiva_admisiones/ver/<pk>', login_required(DESCENInactivaAdmisionDetail.as_view()), name='DESCEN_inactiva_admisiones_ver'),
    # Intervensiones
    path('DESCEN/intervenciones/crear/<pk>', login_required(DESCENIntervencionesCreateView.as_view()), name='DESCEN_intervenciones_crear'),
    path('DESCEN/intervenciones/ver/<pk>', login_required(DESCENIntervencionesLegajosListView.as_view()), name='DESCEN_intervenciones_legajos_listar'),
    path('DESCEN/intervenciones/listar/', login_required(DESCENIntervencionesListView.as_view()), name='DESCEN_intervenciones_listar'),
    path('DESCEN/intervencion/ver/<pk>', login_required(DESCENIntervencionesDetail.as_view()), name='DESCEN_intervencion_ver'),
    path('DESCEN/intervenciones/editar/<pk>', login_required(DESCENIntervencionesUpdateView.as_view()), name='DESCEN_intervencion_editar'),
    path('DESCEN/intervenciones/borrar/<pk>', login_required(DESCENIntervencionesDeleteView.as_view()), name='DESCEN_intervencion_borrar'),
    # Stock
    
    ]

