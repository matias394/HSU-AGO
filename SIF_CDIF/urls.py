from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('CDIF/derivaciones/listar', login_required(CDIFDerivacionesListView.as_view()), name='CDIF_derivaciones_listar'),
    path('CDIF/derivaciones/ver/<pk>', login_required(CDIFDerivacionesDetailView.as_view()), name='CDIF_derivaciones_ver'),
    path('CDIF/preadmisiones/crear/<pk>', login_required(CDIFPreAdmisionesCreateView.as_view()), name='CDIF_preadmisiones_crear'),
    path('CDIF/preadmisiones/editar/<pk>', login_required(CDIFPreAdmisionesUpdateView.as_view()), name='CDIF_preadmisiones_editar'),
    path('CDIF/preadmisiones/ver/<pk>', login_required(CDIFPreAdmisionesDetailView.as_view()), name='CDIF_preadmisiones_ver'),
    path('CDIF/preadmisiones/listar', login_required(CDIFPreAdmisionesListView.as_view()), name='CDIF_preadmisiones_listar'),
    path('CDIF/criterios_ivi/crear', login_required(CDIFCriteriosIVICreateView.as_view()), name='CDIF_criterios_ivi_crear'),
    path('CDIF/indice_ivi/crear/<pk>', login_required(CDIFIndiceIviCreateView.as_view()), name='CDIF_indiceivi_crear'),
    path('CDIF/indice_ivi/ver/<pk>', login_required(CDIFIndiceIviDetailView.as_view()), name='CDIF_indiceivi_ver'),
    path('CDIF/indice_ivi/editar/<pk>', login_required(CDIFIndiceIviUpdateView.as_view()), name='CDIF_indiceivi_editar'),

    ]

