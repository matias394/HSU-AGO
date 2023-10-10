from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('CDIF/derivaciones/listar', login_required(CDIFDerivacionesListView.as_view()), name='CDIF_derivaciones_listar'),
    path('CDIF/derivaciones/ver/<pk>', login_required(CDIFDerivacionesDetailView.as_view()), name='CDIF_derivaciones_ver'),
    path('CDIF/derivaciones/rechazo/<pk>', login_required(CDIFDerivacionesRechazo.as_view()), name='CDIF_derivaciones_rechazo'),
    path('CDIF/preadmisiones/crear/<pk>', login_required(CDIFPreAdmisionesCreateView.as_view()), name='CDIF_preadmisiones_crear'),
    path('CDIF/preadmisiones/editar/<pk>', login_required(CDIFPreAdmisionesUpdateView.as_view()), name='CDIF_preadmisiones_editar'),
    path('CDIF/preadmisiones/ver/<pk>', login_required(CDIFPreAdmisionesDetailView.as_view()), name='CDIF_preadmisiones_ver'),
    path('CDIF/preadmisiones/ver3/<pk>', login_required(CDIFPreAdmisiones3DetailView.as_view()), name='CDIF_preadmisiones_ver3'),
    path('CDIF/preadmisiones/listar', login_required(CDIFPreAdmisionesListView.as_view()), name='CDIF_preadmisiones_listar'),
    path('CDIF/criterios_ivi/crear', login_required(CDIFCriteriosIVICreateView.as_view()), name='CDIF_criterios_ivi_crear'),
    path('CDIF/indice_ivi/crear/<pk>', login_required(CDIFIndiceIviCreateView.as_view()), name='CDIF_indiceivi_crear'),
    path('CDIF/indice_ivi/ver/<pk>', login_required(CDIFIndiceIviDetailView.as_view()), name='CDIF_indiceivi_ver'),
    path('CDIF/indice_ivi/editar/<pk>', login_required(CDIFIndiceIviUpdateView.as_view()), name='CDIF_indiceivi_editar'),
    path('CDIF/vacantes/list/', login_required(CDIFVacantesListView.as_view()), name='CDIF_vacantes_listar'),
    path('CDIF/vacantes_detail/<pk>', login_required(CDIFVacantesDetailView.as_view()), name='CDIF_vacantes_ver'),
    path('CDIF/admisiones_detail/<pk>', login_required(CDIFAdmisionesDetailView.as_view()), name='CDIF_admisiones_ver'),
    path('CDIF/vacantes_form/<pk>', login_required(CDIFVacantesAdmision.as_view()), name='CDIF_vacantes_form'),
    path('CDIF/vacantes_form_cambio/<pk>', login_required(CDIFVacantesAdmisionCambio.as_view()), name='CDIF_vacantes_form_cambio'),
    path('CDIF/asignado_admisiones_detail/<pk>', login_required(CDIFAsignadoAdmisionDetail.as_view()), name='CDIF_asignado_admisiones_ver'),
    path('CDIF/intervenciones_form/<pk>', login_required(CDIFIntervencionesCreateView.as_view()), name='CDIF_intervenciones_crear'),
    path('CDIF/intervenciones_list/<pk>', login_required(CDIFIntervencionesListView.as_view()), name='CDIF_intervenciones_listar'),
    ]

