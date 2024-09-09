from django.db import models
from Configuraciones.models import *
from Legajos.models import *
from django.core.validators import MinValueValidator, MaxValueValidator
from .choices import *
from django.urls import *
from SIF_CDIF.models import Criterios_IVI 
# Create your models here.

#class legajo_CDLE (models.Model):
#    fk_programa = models.ForeignKey(Programas, on_delete=models.PROTECT)
#    fk_legajo = models.ForeignKey(Legajos, on_delete=models.PROTECT)
#    nombre = models.CharField(max_length=100, unique=True)
#    estado = models.BooleanField(default=True)
#    observaciones = models.CharField(max_length=300, null=True, blank=True)
#    #creado_por = models.ForeignKey(Usuarios, related_name='CDLE_creado_por', on_delete=models.PROTECT, blank=True, null=True)
#    #modificado_por = models.ForeignKey(Usuarios, related_name='CDLE_modificado_por', on_delete=models.PROTECT, blank=True, null=True)
#    creado = models.DateField(auto_now_add=True)
#    modificado = models.DateField(auto_now=True)
#
#    def __str__(self):
#        return self.nombre
#
#    def clean(self):
#        self.nombre = self.nombre.capitalize()
#
#    class Meta:
#        ordering = ['nombre']
#        verbose_name = 'Programa'
#        verbose_name_plural = "Programas"
#
#    def get_absolute_url(self):
#        return reverse('programas_ver', kwargs={'pk': self.pk})
    
#class Centros (models.Model):
#    nombre = models.CharField(max_length=250, null=False, blank=False)
#    sala = models.CharField(max_length=250, null=False, blank=False)
#    disponibles = models.IntegerField(null=False, blank=False)
#
#    def __str__(self):
#        return self.nombre
#
#    def clean(self):
#        self.nombre = self.nombre.capitalize()
#
#    class Meta:
#        ordering = ['nombre']
#        verbose_name = 'Centro'
#        verbose_name_plural = "Centros"

class CDLE_PreAdmision (models.Model):
    fk_derivacion = models.ForeignKey(LegajosDerivaciones, on_delete=models.PROTECT)
    fk_legajo = models.ForeignKey(Legajos, related_name='CDLE_fk_legajo', on_delete=models.PROTECT, null=True, blank=True)
    ivi = models.CharField(max_length=150, null=True, blank=True)
    indice_ingreso = models.CharField(max_length=150, null=True, blank=True)
    admitido = models.CharField(max_length=150, null=True, blank=True)
    creado_por = models.ForeignKey(Usuarios, related_name='CDLE_PreAdm_creado_por', on_delete=models.PROTECT, blank=True, null=True)
    modificado_por = models.ForeignKey(Usuarios, related_name='CDLE_PreAdm_modificado_por', on_delete=models.PROTECT, blank=True, null=True)
    creado = models.DateField(auto_now_add=True, null=True, blank=True)
    modificado = models.DateField(auto_now=True, null=True, blank=True)
    estado = models.CharField(max_length=100, null=True, blank=True)
    tipo = models.CharField(max_length=100, null=True, blank=True)
    # 1 Grupo Familiar (Funcionalidad del legajo)
    # 2 Entrevista
    # 3 Embarazo
    # 4 Salud de la embarazada
    # 5 Controles
    # 6 Pareja o apoyo en la crianza
    # 7 Informacion Familiar
    # 7.1 "Ingresos familiares"
    # 8 Acompañante y conclusiones
    # 8.1 Conclusiones (No preguntar)
    # 8.2 Candidata a

    # Paso 1 : Grupo familiar
    # Misma funcionalidad del legajo

    # Paso 2 : Entrevista
    ENTR_fec_entr = models.DateField(verbose_name="Fecha de la entrevista", null=True, blank=True)
    ENTR_barrio_operativo = models.CharField(max_length=150,verbose_name="Barrio de operativo", choices=CHOICE_BARRIOS, null=True, blank=True)
    ENTR_ingreso_por = models.CharField(max_length=150,verbose_name="Ingresó por", choices=CHOICE_INGRESOPOR, null=True, blank=True)
    ENTR_derivacion_de = models.CharField(max_length=150,verbose_name="Derivación de", choices=CHOICE_DERIVACIONDE, null=True, blank=True)
    ENTR_derivacion_otro = models.CharField(max_length=150,verbose_name="Otro", null=True, blank=True)
    ENTR_reinc_en_programa = models.BooleanField(verbose_name="Reincidencia en el programa Si/No", null=True, blank=True)
    # Si se marca que si el campo "Reincidencia en el programa Si/No" se debe ver el campo "Año" Tipo: Año

    # Paso 3 : Embarazo
    EMBA_primer_emba = models.CharField(max_length=150,verbose_name="Primer embarazo", choices=CHOICE_SINO, null=True, blank=True)
    EMBA_fec_ultima_mentru = models.DateField(verbose_name="Fecha última mestruación", null=True, blank=True)
    EMBA_sems_emba = models.CharField(max_length=150,verbose_name="Semanas de embarazo" ,choices=CHOICE_1to40, null=True, blank=True)
    EMBA_fpp = models.DateField(verbose_name="FPP", null=True, blank=True)
    EMBA_centro_salud_controla = models.CharField(max_length=150,verbose_name="Centro de salud que se controla", choices=CHOICE_CENTRO_CONTROL, null=True, blank=True)
    EMBA_obstetrica = models.CharField(max_length=150,verbose_name="Obstétrica", null=True, blank=True)
    EMBA_hizo_test_emba = models.CharField(max_length=150,verbose_name="¿Te hiciste test de embarazo?", choices=CHOICE_SINO, null=True, blank=True)
    EMBA_sem_primer_ctrl = models.CharField(max_length=150,verbose_name="¿Semana del primer control?" ,choices=CHOICE_1to40, null=True, blank=True)
    EMBA_tiene_lib_sanitaria = models.CharField(max_length=150,verbose_name="¿Tiene libreta sanitaria?" , choices=CHOICE_SINO, null=True, blank=True)
    EMBA_recibio_en = models.CharField(max_length=150,verbose_name="Recibió en", null=True, blank=True)
    EMBA_conoce_metod_anticoncep = models.CharField(max_length=150,verbose_name="¿Conoces los métodos anticonceptivos?" , choices=CHOICE_SINO, null=True, blank=True)
    EMBA_list_conoce_metod_anticoncep = models.CharField(max_length=150,verbose_name="¿Cuáles conoces?",choices=CHOICE_METODOS_ANTICONCEPTIVOS, null=True, blank=True)
    EMBA_uso_en_estado_emba = models.CharField(max_length=150,verbose_name="¿Utilizabas alguno cuando quedaste embarazada?" , choices=CHOICE_SINO, null=True, blank=True)
    EMBA_list_uso_en_estado_emba = models.CharField(max_length=150,verbose_name="¿Cuál usabas?",choices=CHOICE_METODOS_ANTICONCEPTIVOS, null=True, blank=True)
    EMBA_sifilis_en_anterior_emba = models.CharField(max_length=150,verbose_name="¿Tuviste sífilis en embarazos anteriores?", choices=CHOICE_SINO, null=True, blank=True)
    EMBA_sifilis_realizo_tratam = models.CharField(max_length=150,verbose_name="¿Realizaste el tratamiento?", choices=CHOICE_RESPONSABLE, null=True, blank=True)
    EMBA_sifilis_tratam_completado = models.CharField(max_length=150,verbose_name="¿Lo completaste?", choices=CHOICE_RESPONSABLE, null=True, blank=True)
    EMBA_sifilis_actual = models.CharField(max_length=150,verbose_name="¿Tenés sífilis actualmente?", choices=CHOICE_SINO, null=True, blank=True)
    EMBA_sifilis_actual_tratamiento = models.CharField(max_length=150,verbose_name="¿Realizaste el tratamiento?", choices=CHOICE_RESPONSABLE, null=True, blank=True)
    EMBA_sifilis_actual_tratamiento_completado = models.CharField(max_length=150,verbose_name="¿Lo completaste?", choices=CHOICE_RESPONSABLE, null=True, blank=True)
    EMBA_sifilis_pareja_tratamiento = models.CharField(max_length=150,verbose_name="¿Tu pareja hizo el tratamiento?", choices=CHOICE_RESPONSABLE, null=True, blank=True)
    EMBA_sifilis_pareja_tratamiento_completado = models.CharField(max_length=150,verbose_name="¿Lo completó?", choices=CHOICE_RESPONSABLE, null=True, blank=True)
    # Sección 3.1 : Antecedentes de embarazo y parto
    EMBA_cantidad_emba = models.SmallIntegerField(verbose_name="Cantidad de embarazos", null=True, blank=True)
    EMBA_cantidad_hijos = models.SmallIntegerField(verbose_name="Cantidad de hijos", null=True, blank=True)
    EMBA_cantidad_menores = models.SmallIntegerField(verbose_name="Menores", null=True, blank=True)
    EMBA_cantidad_mayores = models.SmallIntegerField(verbose_name="Mayores", null=True, blank=True)
    EMBA_cantidad_abortos = models.SmallIntegerField(verbose_name="Cantidad de abortos", null=True, blank=True)
    EMBA_cantidad_abortos_expon = models.SmallIntegerField(verbose_name="Espontáneos", null=True, blank=True)
    EMBA_cantidad_abortos_provoc = models.SmallIntegerField(verbose_name="Provocados", null=True, blank=True)
    # ¿Tiene alguno de estos antecedentes?
    EMBA_check_emba_no_ctrl = models.BooleanField(verbose_name="Embarazo no controlado", null=True, blank=True)
    EMBA_check_emba_adol = models.BooleanField(verbose_name="Embarazo adolescente", null=True, blank=True)
    EMBA_check_emba_riesgo = models.BooleanField(verbose_name="Embarazo de riesgo", null=True, blank=True)
    EMBA_check_cesareas_multi = models.BooleanField(verbose_name="Cesáreas múltiples", null=True, blank=True)
    EMBA_check_partos_multi = models.BooleanField(verbose_name="Partos múltiples", null=True, blank=True)
    EMBA_check_partos_prema = models.BooleanField(verbose_name="Partos prematuros", null=True, blank=True)
    EMBA_check_partos_menos_meses_interval = models.BooleanField(verbose_name="Partos con menos de 18 meses de intervalo", null=True, blank=True)
    EMBA_check_emba_perdidas_recurrentes = models.BooleanField(verbose_name="Perdidas de embarazo recurrentes", null=True, blank=True)
    EMBA_check_feto_muerto = models.BooleanField(verbose_name="Feto muerto", null=True, blank=True)

    # Paso 4 : Salud de la embarazada
    SALUDEMBA_obra_social = models.CharField(max_length=150,verbose_name="Obra Social" , choices=CHOICE_SINO, null=True, blank=True)
    SALUDEMBA_obra_social_desc = models.CharField(max_length=150,verbose_name="¿Cuál?", null=True, blank=True)
    SALUDEMBA_padece_enf_fisica = models.CharField(max_length=150,verbose_name="¿Padece alguna enfermedad física?", choices=CHOICE_SINO, null=True, blank=True)
    SALUDEMBA_padece_enf_fisica_desc = models.CharField(max_length=150,verbose_name="¿Cuál?", null=True, blank=True)
    SALUDEMBA_padece_enf_psiquica = models.CharField(max_length=150,verbose_name="¿Padece alguna enfermedad psíquica?", choices=CHOICE_SINO, null=True, blank=True)
    SALUDEMBA_padece_enf_psiquica_desc = models.CharField(max_length=150,verbose_name="¿Cuál?", null=True, blank=True)
    SALUDEMBA_tratam_x_enf = models.CharField(max_length=150,verbose_name="¿Se encuentra en tratamiento por alguna enfermedad?", choices=CHOICE_SINO, null=True, blank=True)
    SALUDEMBA_tratam_x_enf_desc = models.CharField(max_length=150,verbose_name="¿Donde?", choices=CHOICE_CENTROS_SALUD, null=True, blank=True)
    SALUDEMBA_cap_reducida_o_afec = models.CharField(max_length=150,verbose_name="Capacidad reducida o afectada o CUD", choices=CHOICE_SINO, null=True, blank=True)
    # Sección 4.1 : Salud de la embarazada - Consumo
    SALUDEMBA_consumio_drogas = models.CharField(max_length=150,verbose_name="¿Alguna vez consumió drogas?", choices=CHOICE_SINO, null=True, blank=True)
    SALUDEMBA_consumio_drogas_actual = models.CharField(max_length=150,verbose_name="¿Consume actualmente?", choices=CHOICE_SINO, null=True, blank=True)
    SALUDEMBA_consumio_drogas_desc = models.CharField(max_length=150,verbose_name="¿Cuál?", null=True, blank=True)
    SALUDEMBA_consume_alcohol_actual = models.CharField(max_length=150,verbose_name="¿Consume alcohol actualmente?", choices=CHOICE_SINO, null=True, blank=True)
    SALUDEMBA_sospecha_consumo = models.CharField(max_length=150,verbose_name="¿Sospecha de consumo?", choices=CHOICE_SINO, null=True, blank=True)
    SALUDEMBA_fuma_cigarro_actual = models.CharField(max_length=150,verbose_name="¿Fuma cigarrillo actualmente?", choices=CHOICE_SINO, null=True, blank=True)
    SALUDEMBA_dao = models.CharField(max_length=150,verbose_name="¿DAO+?", choices=CHOICE_SINO, null=True, blank=True)
    SALUDEMBA_momento_consumo = models.CharField(max_length=150,verbose_name="Identifica en qué momento empezó a consumir", null=True, blank=True)
    SALUDEMBA_causa_consumo = models.CharField(max_length=150,verbose_name="Identifica la causa del consumo", null=True, blank=True)

    # Sección 5 : Controles-
    CTRL_fec_aprox_primer_ctrl = models.DateField(verbose_name="Fecha aprox. 1° control", null=True, blank=True)
    CTRL_centro_salud = models.CharField(max_length=150,verbose_name="¿En que centro de salud?", choices=CHOICE_CENTROS_SALUD, null=True, blank=True)
    CTRL_en_cantidad_sem_emba = models.IntegerField(verbose_name="¿A cuantas semanas de embarazo?", choices=CHOICE_1to40, null=True, blank=True)
    CTRL_fec_ultimo_ctrl = models.DateField(verbose_name="Fecha último control", null=True, blank=True)
    CTRL_fec_proximo_ctrl = models.DateField(verbose_name="Fecha próximo control", null=True, blank=True)
    CTRL_emb_controlado = models.CharField(max_length=20, verbose_name="Embarazo controlado", choices=CHOICE_EMBARAZO_CONTROLADO, null=True, blank=True)
    CTRL_check_comienza_control_op = models.BooleanField(verbose_name="¿Comienza control en operativo?", null=True, blank=True)
    # "Primer Trimestre (0-14 semanas)"
    CTRL_check_pt_obstetra = models.BooleanField(verbose_name="Al menos 1 control con la obstetra", null=True, blank=True)
    CTRL_check_pt_laboratorio = models.BooleanField(verbose_name="Laboratorio- Rutina 1er trimestre", null=True, blank=True)
    CTRL_check_pt_ecografia = models.BooleanField(verbose_name="Ecografía", null=True, blank=True)
    CTRL_check_pt_pap = models.BooleanField(verbose_name="PAP", null=True, blank=True)
    CTRL_check_pt_grupofactor = models.BooleanField(verbose_name="Grupo y Factor", null=True, blank=True)
    CTRL_check_pt_odontologico = models.BooleanField(verbose_name="Control odontologico", null=True, blank=True)
    # "Segundo Trimestre (15 a 28 semanas), 
    CTRL_check_st_obstetra = models.BooleanField(verbose_name="Al menos 2 controles con la obstetra", null=True, blank=True)
    CTRL_check_st_scanfetal = models.BooleanField(verbose_name="Scan fetal", null=True, blank=True)
    CTRL_check_st_p75 = models.BooleanField(verbose_name="P75", null=True, blank=True)
    # "Tercer Trimestre (29 a 41 semanas)".
    CTRL_check_tt_obstetra = models.BooleanField(verbose_name="Al menos 5 controles con la obstetra", null=True, blank=True)
    CTRL_check_tt_eco_hiso_labo = models.BooleanField(verbose_name="Ecografía, hisopado vaginal y laboratorio", null=True, blank=True)
    CTRL_check_tt_monitoreo_fetal = models.BooleanField(verbose_name="Monitoreo fetal", null=True, blank=True)
    CTRL_check_tt_electrocardio = models.BooleanField(verbose_name="Electro cardiograma", null=True, blank=True)


    # Paso 6 : "Pareja o apoyo en la crianza" (Igual a "Padre o apoyo en la crianza, cambiar el nombre del Paso)
    # 6.1 DATOS PERSONALES
    POACRI_pareja_apoyo_crianza = models.CharField(max_length=150,verbose_name="Padre o apoyo en la crianza", null=True, blank=True)
    POACRI_vinculo = models.CharField(max_length=150,verbose_name="Vínculo", null=True, blank=True)
    POACRI_tipo_doc = models.CharField(max_length=150,verbose_name="Tipo de documento", null=True, blank=True)
    POACRI_num_doc = models.CharField(max_length=150,verbose_name="Numero documento", null=True, blank=True)
    # 6.2 EDUCACION
    POACRI_edu_max_nivel = models.CharField(max_length=150,verbose_name="Máximo nivel alcanzado", choices=CHOICE_NIVEL_EDUCATIVO, null=True, blank=True)
    POACRI_edu_estado = models.CharField(max_length=150,verbose_name="Estado", choices=CHOICE_ESTADO_NIVEL_EDUCATIVO, null=True, blank=True)
    POACRI_check_edu_sabe_leer = models.BooleanField(verbose_name="Sabe leer", null=True, blank=True)
    POACRI_check_edu_sabe_escribir = models.BooleanField(verbose_name="Sabe escribir", null=True, blank=True)
    POACRI_check_edu_quiere_retomar_estudios = models.BooleanField(verbose_name="Quiere retomar estudios", null=True, blank=True)
    POACRI_check_edu_quiere_aprender_oficio = models.BooleanField(verbose_name="Quiere aprender un oficio", null=True, blank=True)
    POACRI_check_edu_quiere_parti_prog_pilates = models.BooleanField(verbose_name="Quiere participar del Programa Pilares", null=True, blank=True)
    # 6.3 ECONOMIA
    POACRI_eco_planes_sociales_recibe = models.ForeignKey(PlanesSociales,verbose_name="Planes sociales que recibe", on_delete=models.PROTECT, null=True, blank=True)
    
    # 6.4 TRABAJO
    POACRI_trab_tiene_trabajo_actual = models.CharField(max_length=150,verbose_name="¿Tiene trabajo actualmente?", choices=CHOICE_SINO, null=True, blank=True)
    POACRI_trab_ocupacion = models.CharField(max_length=150,verbose_name="Ocupación", null=True, blank=True)
    POACRI_trab_modo_contratacion = models.CharField(max_length=150,verbose_name="Modo de contratación", choices=CHOICE_MODO_CONTRATACION, null=True, blank=True)


    # Paso 7. "Información Familiar"
    INFOFAMI_check_convivientes_tienen_dni = models.BooleanField(verbose_name="¿Todos los convivientes tienen DNI?" , null=True, blank=True)
    INFOFAMI_convivientes_tienen_dni_desc = models.CharField(max_length=150,verbose_name="Datos", null=True, blank=True)
    INFOFAMI_check_menores_escolarizados = models.BooleanField(verbose_name="¿Todos los menores de 18 años están escolarizados?" , null=True, blank=True)
    INFOFAMI_menores_escolarizados_desc = models.CharField(max_length=150,verbose_name="Datos", null=True, blank=True)
    INFOFAMI_check_menor_con_bajopes_sobrepes = models.BooleanField(verbose_name="¿Hay algún menor de edad con bajo peso o sobrepeso?" , null=True, blank=True)
    INFOFAMI_menor_con_bajopes_sobrepes_desc = models.CharField(max_length=150,verbose_name="Datos", null=True, blank=True)
    INFOFAMI_check_menor_con_ante_acci_dom = models.BooleanField(verbose_name="¿Hay algún menor de edad con antecedentes de accidentes domésticos graves o a repetición?" , null=True, blank=True)
    INFOFAMI_menor_con_ante_acci_dom_desc = models.CharField(max_length=150,verbose_name="Datos", null=True, blank=True)
    INFOFAMI_check_menor_con_ante_acci_dom_seguimiento = models.BooleanField(verbose_name="¿En seguimiento?" , null=True, blank=True)
    INFOFAMI_check_menores_con_ctrl_vacunas = models.BooleanField(verbose_name="¿Todos los menores de 18 tienen controles de salud y vacunas correspondientes?" , null=True, blank=True)
    INFOFAMI_menores_con_ctrl_vacunas_desc = models.CharField(max_length=150,verbose_name="Datos", null=True, blank=True)
    INFOFAMI_check_menor_con_patologia = models.BooleanField(verbose_name="¿Algún menor de 18 años padece una patología?" , null=True, blank=True)
    INFOFAMI_check_menor_con_patologia_seguimiento = models.BooleanField(verbose_name="¿En seguimiento?" , null=True, blank=True)
    INFOFAMI_menor_con_patologia_desc = models.CharField(max_length=150,verbose_name="Datos", null=True, blank=True)
    INFOFAMI_check_menor_capas_reduc_afec = models.BooleanField(verbose_name="¿Hay algún menor de edad con capacidades reducidas o afectadas (CUD)?" , null=True, blank=True)
    INFOFAMI_menor_capas_reduc_afec_desc = models.CharField(max_length=150,verbose_name="Datos", null=True, blank=True)
    INFOFAMI_conviviente_enf_infec_contagiosa = models.CharField(max_length=150,verbose_name="¿Hay algún conviviente con enfermedad infecto-contagiosa? (tuberculosis, sarampión, sífilis, HIV)", choices=CHOICE_SINO, null=True, blank=True)
    INFOFAMI_conviviente_enf_infec_contagiosa_desc = models.CharField(max_length=150,verbose_name="Datos", null=True, blank=True)
    INFOFAMI_check_conviviente_consum_drogas = models.BooleanField(verbose_name="¿Hay algún conviviente con consumo problemático de sustancias o sospecha de consumo?" , null=True, blank=True)
    INFOFAMI_conviviente_consum_drogas_desc = models.CharField(max_length=150,verbose_name="Datos", null=True, blank=True)
    INFOFAMI_check_emba_con_situacion_conflicto = models.BooleanField(verbose_name="¿La embarazada atraviesa o atravesó alguna situación conflictiva, de violencia o problema legal?" , null=True, blank=True)
    INFOFAMI_check_emba_con_situacion_conflicto_denuncio = models.BooleanField(verbose_name="¿Denunció?" , null=True, blank=True)
    INFOFAMI_check_emba_con_situacion_conflicto_protegida = models.BooleanField(verbose_name="¿Protegida por medida judicial/perimetral?" , null=True, blank=True)
    INFOFAMI_emba_con_situacion_conflicto_desc = models.CharField(max_length=150,verbose_name="Datos", null=True, blank=True)
    INFOFAMI_check_familiar_con_problema_legal = models.BooleanField(verbose_name="¿Algún integrante de la familia tiene un problema legal?" , null=True, blank=True)
    INFOFAMI_familiar_con_problema_legal_desc = models.CharField(max_length=150,verbose_name="Detallar", null=True, blank=True)
    INFOFAMI_check_familiar_con_problema_legal_denuncio = models.BooleanField(verbose_name="¿Denunciaron esta situación?" , null=True, blank=True)
    INFOFAMI_check_antecedente_duelo_trauma_reciente = models.BooleanField(verbose_name="¿Presentan antecedentes de duelo o situación traumática reciente?" , null=True, blank=True)
    # Seccion 7.1. "Ingresos familiares" (dentro del paso 6)
    INFOFAMI_ingreso_aprox = models.IntegerField(verbose_name="Ingresos aprox. mensuales del grupo familiar", null=True, blank=True)
    INFOFAMI_check_ingresos_plan_social = models.BooleanField(verbose_name="¿Sus ingresos son exclusivamente de planes sociales?", null=True, blank=True)
    INFOFAMI_check_ingreso_alcanza_alimentos = models.BooleanField(verbose_name="¿El dinero les alcanza para comer?", null=True, blank=True)
    INFOFAMI_veces_comen_aldia = models.IntegerField(verbose_name="¿Cuántas veces al día comen una comida completa?", choices=CHOICE_1to4, null=True, blank=True)

    # Paso 8: "Acompañante y conclusiones"
    # Sección 8.1"Conclusiones (No preguntar)"
    CONCLUS_check_cuidador_tiene_red_proteccion = models.BooleanField(verbose_name="Madre o cuidador principal tiene red de contención", null=True, blank=True)
    CONCLUS_check_mujer_falta_valoracion = models.BooleanField(verbose_name="Mujer con falta de autovaloración", null=True, blank=True)
    CONCLUS_check_dificultad_vinculo_crianza = models.BooleanField(verbose_name="Tiene dificultad en el vínculo y la crianza", null=True, blank=True)
    CONCLUS_check_dificultad_compr_com = models.BooleanField(verbose_name="Tiene dificultad para la comprensión y la comunicación", null=True, blank=True)
    CONCLUS_check_adh_sis_salud = models.BooleanField(verbose_name="Tiene adherencia al sistema de salud y lleva a los niños a los controles", null=True, blank=True)
    CONCLUS_check_fam_acceso_limitado_info = models.BooleanField(verbose_name="Familia con acceso limitado a la información", null=True, blank=True)

    # Sección 8.2 : Candidata a:
    CONCLUS_check_recibir_catre = models.BooleanField(verbose_name="Recibir catre", null=True, blank=True)
    CONCLUS_participar_de = models.CharField(max_length=150,verbose_name="Participar de", choices=CHOISE_CDLE_PARTICIPARDE, null=True, blank=True)
    #SubTexto ; aclaración "Derivar el legajo en caso de ser candidata"
    CONCLUS_acompaniante = models.CharField(max_length=150,verbose_name="Acompañante", choices=CHOISE_CDLE_ACOMPANIANTES, null=True, blank=True)

# class Criterios_IVI(models.Model):
#     criterio =  models.CharField(max_length=250, null=False, blank=False)
#     tipo =  models.CharField(max_length=250, choices=CHOICE_TIPO_IVI, null=False, blank=False)
#     puntaje =  models.SmallIntegerField(null=False, blank=False)
#     modificable =  models.CharField(max_length=50, choices=CHOICE_NOSI, null=False, blank=False)
    
#     def __str__(self):
#         return self.criterio

class CDLE_IndiceIVI(models.Model):
    fk_criterios_ivi = models.ForeignKey(Criterios_IVI, on_delete=models.PROTECT)
    fk_legajo = models.ForeignKey(Legajos, on_delete=models.PROTECT, null=True, blank=True)
    fk_preadmi = models.ForeignKey(CDLE_PreAdmision, on_delete=models.PROTECT, null=True, blank=True)
    presencia = models.BooleanField (default=False, null=True, blank=True)
    tipo = models.CharField (max_length=350, null=True, blank=True)
    programa = models.CharField(max_length=150, choices=CHOICE_NOSI, null=True, blank=True)
    clave = models.CharField (max_length=350, null=True, blank=True)
    creado = models.DateField(auto_now_add=True, null=True, blank=True)
    modificado = models.DateField(auto_now=True, null=True, blank=True)

class CDLE_Foto_IVI(models.Model):
    fk_preadmi = models.ForeignKey(CDLE_PreAdmision, on_delete=models.PROTECT, null=True, blank=True)
    fk_legajo = models.ForeignKey(Legajos, on_delete=models.PROTECT, null=True, blank=True)
    puntaje = models.SmallIntegerField(null=True, blank=True) 
    puntaje_max = models.SmallIntegerField(null=True, blank=True)
    crit_modificables = models.SmallIntegerField(null=True, blank=True)
    crit_presentes = models.SmallIntegerField(null=True, blank=True)
    observaciones = models.CharField(max_length=350, null=True, blank=True)
    tipo = models.CharField (max_length=350, null=True, blank=True)
    clave = models.CharField (max_length=350, null=True, blank=True)
    creado_por = models.ForeignKey(Usuarios, related_name='CDLE_IVI_creado_por', on_delete=models.PROTECT, blank=True, null=True)
    modificado_por = models.ForeignKey(Usuarios, related_name='CDLE_IVI_modificado_por', on_delete=models.PROTECT, blank=True, null=True)
    creado = models.DateField(auto_now_add=True, null=True, blank=True)
    modificado = models.DateField(auto_now=True, null=True, blank=True)

class Criterios_Ingreso(models.Model):
    criterio =  models.CharField(max_length=250, null=False, blank=False)
    tipo =  models.CharField(max_length=250, choices=CHOICE_TIPO_INGRESO, null=False, blank=False)
    puntaje =  models.SmallIntegerField(null=False, blank=False)
    modificable =  models.CharField(max_length=50, choices=CHOICE_NOSI, null=False, blank=False)
    
    def __str__(self):
        return self.criterio

class CDLE_IndiceIngreso(models.Model):
    fk_criterios_ingreso = models.ForeignKey(Criterios_Ingreso, on_delete=models.PROTECT)
    fk_legajo = models.ForeignKey(Legajos, on_delete=models.PROTECT, null=True, blank=True)
    fk_preadmi = models.ForeignKey(CDLE_PreAdmision, on_delete=models.PROTECT, null=True, blank=True)
    presencia = models.BooleanField (default=False, null=True, blank=True)
    tipo = models.CharField (max_length=350, null=True, blank=True)
    programa = models.CharField(max_length=150, choices=CHOICE_NOSI, null=True, blank=True)
    clave = models.CharField (max_length=350, null=True, blank=True)
    creado = models.DateField(auto_now_add=True, null=True, blank=True)
    modificado = models.DateField(auto_now=True, null=True, blank=True)

class CDLE_Foto_Ingreso(models.Model):
    fk_preadmi = models.ForeignKey(CDLE_PreAdmision, on_delete=models.PROTECT, null=True, blank=True)
    fk_legajo = models.ForeignKey(Legajos, on_delete=models.PROTECT, null=True, blank=True)
    puntaje = models.SmallIntegerField(null=True, blank=True) 
    puntaje_max = models.SmallIntegerField(null=True, blank=True)
    crit_modificables = models.SmallIntegerField(null=True, blank=True)
    crit_presentes = models.SmallIntegerField(null=True, blank=True)
    observaciones = models.CharField(max_length=350, null=True, blank=True)
    tipo = models.CharField (max_length=350, null=True, blank=True)
    clave = models.CharField (max_length=350, null=True, blank=True)
    creado_por = models.ForeignKey(Usuarios, related_name='CDLE_Ingreso_creado_por', on_delete=models.PROTECT, blank=True, null=True)
    modificado_por = models.ForeignKey(Usuarios, related_name='CDLE_Ingreso_modificado_por', on_delete=models.PROTECT, blank=True, null=True)
    creado = models.DateField(auto_now_add=True, null=True, blank=True)
    modificado = models.DateField(auto_now=True, null=True, blank=True)



class CDLE_Admision(models.Model):
    fk_preadmi = models.ForeignKey(CDLE_PreAdmision, on_delete=models.PROTECT)
    estado = models.CharField(max_length=150, null=True, blank=True, default="Activa")
    creado = models.DateField(auto_now_add=True, null=True, blank=True)
    modificado = models.DateField(auto_now=True, null=True, blank=True)
    creado_por = models.ForeignKey(Usuarios, related_name='CDLE_Admision_creado_por', on_delete=models.PROTECT, blank=True, null=True)
    modificado_por = models.ForeignKey(Usuarios, related_name='CDLE_Admision_modificada_por', on_delete=models.PROTECT, blank=True, null=True)

class OpcionesResponsables(models.Model):
    nombre = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.nombre


class CDLE_Intervenciones(models.Model):
    fk_admision = models.ForeignKey(CDLE_Admision, on_delete=models.PROTECT, null=True, blank=True)
    criterio_modificable = models.ForeignKey(Criterios_IVI, on_delete=models.PROTECT)
    accion = models.CharField(max_length=250, choices=CHOICE_ACCION_DESARROLLADA, null=False, blank=False)
    responsable = models.ManyToManyField(OpcionesResponsables)
    impacto = models.CharField(max_length=250, choices=[('Trabajado','Trabajado'),('Revertido','Revertido')], null=False, blank=False)
    detalle = models.CharField(max_length=350, null=True, blank=True, verbose_name='Observaciones')
    creado = models.DateField(auto_now_add=True, null=True, blank=True)
    modificado = models.DateField(auto_now=True, null=True, blank=True)
    creado_por = models.ForeignKey(Usuarios, related_name='CDLE_Intervenciones_creado_por', on_delete=models.PROTECT, blank=True, null=True)
    modificado_por = models.ForeignKey(Usuarios, related_name='CDLE_Intervenciones_modificada_por', on_delete=models.PROTECT, blank=True, null=True)
    fecha = models.DateField(null=True, blank=True)

class CDLE_Historial(models.Model):
    fk_legajo = models.ForeignKey(Legajos, on_delete=models.PROTECT, null=True, blank=True)
    fk_legajo_derivacion = models.ForeignKey(LegajosDerivaciones, on_delete=models.PROTECT, null=True, blank=True)
    fk_preadmi = models.ForeignKey(CDLE_PreAdmision, on_delete=models.PROTECT, null=True, blank=True)
    fk_admision = models.ForeignKey(CDLE_Admision, on_delete=models.PROTECT, null=True, blank=True)
    movimiento = models.CharField(max_length=150, null=True, blank=True)
    creado = models.DateField(auto_now_add=True, null=True, blank=True)
    creado_por = models.ForeignKey(Usuarios, on_delete=models.PROTECT, null=True, blank=True)

