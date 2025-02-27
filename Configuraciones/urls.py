from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    # Secretarias
    path('configuracion/secretarias/crear', login_required(SecretariasCreateView.as_view()), name='secretarias_crear'),
    path('configuracion/secretarias/listar', login_required(SecretariasListView.as_view()), name='secretarias_listar'),
    path('configuracion/secretarias/ver/<pk>', login_required(SecretariasDetailView.as_view()), name='secretarias_ver'),
    path('configuracion/secretarias/editar/<pk>', login_required(SecretariasUpdateView.as_view()), name='secretarias_editar'),
    path('configuracion/secretarias/eliminar/<pk>', login_required(SecretariasDeleteView.as_view()), name='secretarias_eliminar'),
    # Subsecretarias
    path('configuracion/subsecretarias/crear', login_required(SubsecretariasCreateView.as_view()), name='subsecretarias_crear'),
    path('configuracion/subsecretarias/listar', login_required(SubsecretariasListView.as_view()), name='subsecretarias_listar'),
    path('configuracion/subsecretarias/ver/<pk>', login_required(SubsecretariasDetailView.as_view()), name='subsecretarias_ver'),
    path('configuracion/subsecretarias/editar/<pk>', login_required(SubsecretariasUpdateView.as_view()), name='subsecretarias_editar'),
    path('configuracion/subsecretarias/eliminar/<pk>', login_required(SubsecretariasDeleteView.as_view()), name='subsecretarias_eliminar'),
    # Organismos
    path('configuracion/organismos/crear', login_required(OrganismosCreateView.as_view()), name='organismos_crear'),
    path('configuracion/organismos/listar', login_required(OrganismosListView.as_view()), name='organismos_listar'),
    path('configuracion/organismos/ver/<pk>', login_required(OrganismosDetailView.as_view()), name='organismos_ver'),
    path('configuracion/organismos/editar/<pk>', login_required(OrganismosUpdateView.as_view()), name='organismos_editar'),
    path('configuracion/organismos/eliminar/<pk>', login_required(OrganismosDeleteView.as_view()), name='organismos_eliminar'),
    # Programas
    path('configuracion/programas/crear', login_required(ProgramasCreateView.as_view()), name='programas_crear'),
    path('configuracion/programas/listar', login_required(ProgramasListView.as_view()), name='programas_listar'),
    path('configuracion/programas/ver/<pk>', login_required(ProgramasDetailView.as_view()), name='programas_ver'),
    path('configuracion/programas/editar/<pk>', login_required(ProgramasUpdateView.as_view()), name='programas_editar'),
    path('configuracion/programas/eliminar/<pk>', login_required(ProgramasDeleteView.as_view()), name='programas_eliminar'),
    # PlanesSociales
    path('configuracion/planes_sociales/crear', login_required(PlanesSocialesCreateView.as_view()), name='planes_sociales_crear'),
    path('configuracion/planes_sociales/listar', login_required(PlanesSocialesListView.as_view()), name='planes_sociales_listar'),
    path('configuracion/planes_sociales/ver/<pk>', login_required(PlanesSocialesDetailView.as_view()), name='planes_sociales_ver'),
    path('configuracion/planes_sociales/editar/<pk>', login_required(PlanesSocialesUpdateView.as_view()), name='planes_sociales_editar'),
    path('configuracion/planes_sociales/eliminar/<pk>', login_required(PlanesSocialesDeleteView.as_view()), name='planes_sociales_eliminar'),
    # Agentes Externos
    path('configuracion/agentesexternos/crear', login_required(AgentesExternosCreateView.as_view()), name='agentesexternos_crear'),
    path('configuracion/agentesexternos/crear/<pk>?', login_required(AgentesExternosCreateView.as_view()), name='agentesexternos_crear'),
    path('configuracion/agentesexternos/listar', login_required(AgentesExternosListView.as_view()), name='agentesexternos_listar'),
    path('configuracion/agentesexternos/ver/<pk>', login_required(AgentesExternosDetailView.as_view()), name='agentesexternos_ver'),
    path('configuracion/agentesexternos/editar/<pk>', login_required(AgentesExternosUpdateView.as_view()), name='agentesexternos_editar'),
    path('configuracion/agentesexternos/eliminar/<pk>', login_required(AgentesExternosDeleteView.as_view()), name='agentesexternos_eliminar'),
    # GruposDestinatarios
    path('configuracion/gruposdestinatarios/crear', login_required(GruposDestinatariosCreateView.as_view()), name='gruposdestinatarios_crear'),
    path('configuracion/gruposdestinatarios/listar', login_required(GruposDestinatariosListView.as_view()), name='gruposdestinatarios_listar'),
    path('configuracion/gruposdestinatarios/ver/<pk>', login_required(GruposDestinatariosDetailView.as_view()), name='gruposdestinatarios_ver'),
    path('configuracion/gruposdestinatarios/editar/<pk>', login_required(GruposDestinatariosUpdateView.as_view()), name='gruposdestinatarios_editar'),
    path('configuracion/gruposdestinatarios/eliminar/<pk>', login_required(GruposDestinatariosDeleteView.as_view()), name='gruposdestinatarios_eliminar'),
    # CategoriaAlertas
    path('configuracion/categoriaalertas/crear', login_required(CategoriaAlertasCreateView.as_view()), name='categoriaalertas_crear'),
    path('configuracion/categoriaalertas/listar', login_required(CategoriaAlertasListView.as_view()), name='categoriaalertas_listar'),
    path('configuracion/categoriaalertas/ver/<pk>', login_required(CategoriaAlertasDetailView.as_view()), name='categoriaalertas_ver'),
    path('configuracion/categoriaalertas/editar/<pk>', login_required(CategoriaAlertasUpdateView.as_view()), name='categoriaalertas_editar'),
    path('configuracion/categoriaalertas/eliminar/<pk>', login_required(CategoriaAlertasDeleteView.as_view()), name='categoriaalertas_eliminar'),
    # Alertas
    path('configuracion/alertas/crear', login_required(AlertasCreateView.as_view()), name='alertas_crear'),
    path('configuracion/alertas/listar', login_required(AlertasListView.as_view()), name='alertas_listar'),
    path('configuracion/alertas/ver/<pk>', login_required(AlertasDetailView.as_view()), name='alertas_ver'),
    path('configuracion/alertas/editar/<pk>', login_required(AlertasUpdateView.as_view()), name='alertas_editar'),
    path('configuracion/alertas/eliminar/<pk>', login_required(AlertasDeleteView.as_view()), name='alertas_eliminar'),
    # Equipos
    path('configuracion/equipos/crear', login_required(EquiposCreateView.as_view()), name='equipos_crear'),
    path('configuracion/equipos/listar', login_required(EquiposListView.as_view()), name='equipos_listar'),
    path('configuracion/equipos/ver/<pk>', login_required(EquiposDetailView.as_view()), name='equipos_ver'),
    path('configuracion/equipos/editar/<pk>', login_required(EquiposUpdateView.as_view()), name='equipos_editar'),
    path('configuracion/equipos/eliminar/<pk>', login_required(EquiposDeleteView.as_view()), name='equipos_eliminar'),
    # Acciones
    path('configuracion/acciones/crear', login_required(AccionesCreateView.as_view()), name='acciones_crear'),
    path('configuracion/acciones/listar', login_required(AccionesListView.as_view()), name='acciones_listar'),
    path('configuracion/acciones/ver/<pk>', login_required(AccionesDetailView.as_view()), name='acciones_ver'),
    path('configuracion/acciones/editar/<pk>', login_required(AccionesUpdateView.as_view()), name='acciones_editar'),
    path('configuracion/acciones/eliminar/<pk>', login_required(AccionesDeleteView.as_view()), name='acciones_eliminar'),
    # Criterios
    path('configuracion/criterios/crear', login_required(CriteriosCreateView.as_view()), name='criterios_crear'),
    path('configuracion/criterios/listar', login_required(CriteriosListView.as_view()), name='criterios_listar'),
    path('configuracion/criterios/ver/<pk>', login_required(CriteriosDetailView.as_view()), name='criterios_ver'),
    path('configuracion/criterios/editar/<pk>', login_required(CriteriosUpdateView.as_view()), name='criterios_editar'),
    path('configuracion/criterios/eliminar/<pk>', login_required(CriteriosDeleteView.as_view()), name='criterios_eliminar'),
    # Indices
    path('configuracion/indices/crear', login_required(IndicesCreateView.as_view()), name='indices_crear'),
    path('configuracion/indices/listar', login_required(IndicesListView.as_view()), name='indices_listar'),
    path('configuracion/indices/ver/<pk>', login_required(IndicesDetailView.as_view()), name='indices_ver'),
    path('configuracion/indices/editar/<pk>', login_required(IndicesUpdateView.as_view()), name='indices_editar'),
    path('configuracion/indices/eliminar/<pk>', login_required(IndicesDeleteView.as_view()), name='indices_eliminar'),
    path('delete-variant/<int:pk>/', delete_variant, name='delete_variant'),
    # vacantes
    path('configuracion/vacantes/crear', login_required(VacantesCreateView.as_view()), name='vacantes_crear'),
    path('configuracion/vacantes/listar', login_required(VacantesListView.as_view()), name='vacantes_listar'),
    path('configuracion/vacantes/ver/<pk>', login_required(VacantesDetailView.as_view()), name='vacantes_ver'),
    path('configuracion/vacantes/editar/<pk>', login_required(VacantesUpdateView.as_view()), name='vacantes_editar'),
    path('configuracion/vacantes/eliminar/<pk>', login_required(VacantesDeleteView.as_view()), name='vacantes_eliminar'),
    path('delete-variant/<int:pk>/', delete_variant, name='delete_variant'),
    # Servicio Local Equipos
    path('configuracion/sl_equipos/crear', login_required(SLEquiposCreateView.as_view()), name='slequipos_crear'),
    path('configuracion/sl_equipos/listar', login_required(SLEquiposListView.as_view()), name='slequipos_listar'),
    path('configuracion/sl_equipos/ver/<pk>', login_required(SLEquiposDetailView.as_view()), name='slequipos_ver'),
    path('configuracion/sl_equipos/editar/<pk>', login_required(SLEquiposUpdateView.as_view()), name='slequipos_editar'),
    path('configuracion/sl_equipos/eliminar/<pk>', login_required(SLEquiposDeleteView.as_view()), name='slequipos_eliminar'),
    # Servicio Local Indices Vulnerabilidad
    path('configuracion/sl_indicesvulnerabilidad/crear', login_required(SLIndicesVulnerabilidadCreateView.as_view()), name='slindicesvulnerabilidad_crear'),
    path('configuracion/sl_indicesvulnerabilidad/listar', login_required(SLIndicesVulnerabilidadListView.as_view()), name='slindicesvulnerabilidad_listar'),
    path('configuracion/sl_indicesvulnerabilidad/ver/<pk>', login_required(SLIndicesVulnerabilidadDetailView.as_view()), name='slindicesvulnerabilidad_ver'),
    path('configuracion/sl_indicesvulnerabilidad/editar/<pk>', login_required(SLIndicesVulnerabilidadUpdateView.as_view()), name='slindicesvulnerabilidad_editar'),
    path('configuracion/sl_indicesvulnerabilidad/eliminar/<pk>', login_required(SLIndicesVulnerabilidadDeleteView.as_view()), name='slindicesvulnerabilidad_eliminar'),
]
