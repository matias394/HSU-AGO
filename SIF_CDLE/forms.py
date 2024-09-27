from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit,Div,HTML,Button,Row,Column
from .validators import MaxSizeFileValidator
from SIF_CDIF.models import Criterios_IVI
from .models import *

class CDLE_PreadmisionesForm (forms.ModelForm):
    
    
    def __init__(self, *args, **kwargs):
        legajo: Legajos = kwargs.pop('legajo', None)
        super().__init__(*args, **kwargs)

        if legajo:
            busqueda = Legajos.objects.filter(
                models.Q(fk_legajo1__fk_legajo_2=legajo.id)|
                models.Q(fk_legajo2__fk_legajo_1=legajo.id)
            ).distinct()
            self.fields['POACRI_fk_pareja_apoyo_crianza'].queryset = busqueda

    class Meta:
        model = CDLE_PreAdmision
        fields = '__all__'
        
        widgets = {
            # # Paso 1 : Grupo familiar
            # # Misma funcionalidad del legajo

            # # Paso 2 : Entrevista
            'ENTR_fec_entr' : forms.DateInput(attrs={'type': 'date'}, format="%d-%m-%Y"),
            # 'ENTR_barrio_operativo',
            # 'ENTR_ingreso_por',
            # 'ENTR_derivacion_de',
            # 'ENTR_derivacion_otro',
            # 'ENTR_reinc_en_programa',
            # # Si se marca que si el campo "Reincidencia en el programa Si/No" se debe ver el campo "Año" Tipo: Año
            'ENTR_reinc_en_programa_anio': forms.NumberInput(attrs={'min': '0'}),
            
            # # Paso 3 : Embarazo
            # 'EMBA_primer_emba',
            'EMBA_fec_ultima_mentru' : forms.DateInput(attrs={'type': 'date'}, format="%d-%m-%Y"),
            # 'EMBA_sems_emba',
            'EMBA_fpp': forms.DateInput(attrs={'type': 'date'}, format="%d-%m-%Y"),
            # 'EMBA_centro_salud_controla',
            # 'EMBA_obstetrica',
            # 'EMBA_hizo_test_emba',
            # 'EMBA_sem_primer_ctrl',
            # 'EMBA_tiene_lib_sanitaria',
            # 'EMBA_recibio_en',
            # 'EMBA_conoce_metod_anticoncep',
            'EMBA_list_conoce_metod_anticoncep': forms.SelectMultiple(),
            # 'EMBA_uso_en_estado_emba',
            'EMBA_list_uso_en_estado_emba': forms.SelectMultiple(),
            # 'EMBA_sifilis_en_anterior_emba',
            # 'EMBA_sifilis_realizo_tratam',
            # 'EMBA_sifilis_tratam_completado',
            # 'EMBA_sifilis_actual',
            # 'EMBA_sifilis_actual_tratamiento',
            # 'EMBA_sifilis_actual_tratamiento_completado',
            # 'EMBA_sifilis_pareja_tratamiento',
            # 'EMBA_sifilis_pareja_tratamiento_completado',
            # # Sección 3.1 : Antecedentes de embarazo y parto
            'EMBA_cantidad_emba' : forms.NumberInput(attrs={'min': '0'}),
            'EMBA_cantidad_hijos': forms.NumberInput(attrs={'min': '0'}),
            'EMBA_cantidad_menores': forms.NumberInput(attrs={'min': '0'}),
            'EMBA_cantidad_mayores': forms.NumberInput(attrs={'min': '0'}),
            'EMBA_cantidad_abortos': forms.NumberInput(attrs={'min': '0'}),
            'EMBA_cantidad_abortos_expon': forms.NumberInput(attrs={'min': '0'}),
            'EMBA_cantidad_abortos_provoc': forms.NumberInput(attrs={'min': '0'}),
            # # ¿Tiene alguno de estos antecedentes?
            'EMBA_check_emba_no_ctrl': forms.CheckboxInput(),
            'EMBA_check_emba_adol': forms.CheckboxInput(),
            'EMBA_check_emba_riesgo': forms.CheckboxInput(),
            'EMBA_check_cesareas_multi': forms.CheckboxInput(),
            'EMBA_check_partos_multi': forms.CheckboxInput(),
            'EMBA_check_partos_prema': forms.CheckboxInput(),
            'EMBA_check_partos_menos_meses_interval': forms.CheckboxInput(),
            'EMBA_check_emba_perdidas_recurrentes': forms.CheckboxInput(),
            'EMBA_check_feto_muerto': forms.CheckboxInput(),

            # # Paso 4 : Salud de la embarazada
            # 'SALUDEMBA_obra_social',
            # 'SALUDEMBA_obra_social_desc',
            # 'SALUDEMBA_padece_enf_fisica',
            # 'SALUDEMBA_padece_enf_fisica_desc',
            # 'SALUDEMBA_padece_enf_psiquica',
            # 'SALUDEMBA_padece_enf_psiquica_desc',
            # 'SALUDEMBA_tratam_x_enf',
            # 'SALUDEMBA_tratam_x_enf_desc',
            # 'SALUDEMBA_cap_reducida_o_afec',
            # # Sección 4.1 : Salud de la embarazada - Consumo
            # 'SALUDEMBA_consumio_drogas',
            # 'SALUDEMBA_consumio_drogas_actual',
            # 'SALUDEMBA_consumio_drogas_desc',
            # 'SALUDEMBA_consume_alcohol_actual',
            # 'SALUDEMBA_sospecha_consumo',
            # 'SALUDEMBA_fuma_cigarro_actual',
            # 'SALUDEMBA_dao',
            # 'SALUDEMBA_momento_consumo',
            # 'SALUDEMBA_causa_consumo',

            # # Sección 5 : Controles-
            'CTRL_fec_aprox_primer_ctrl': forms.DateInput(attrs={'type': 'date'}, format="%d-%m-%Y"),
            # 'CTRL_centro_salud',
            # 'CTRL_en_cantidad_sem_emba',
            'CTRL_fec_ultimo_ctrl': forms.DateInput(attrs={'type': 'date'}, format="%d-%m-%Y"),
            'CTRL_fec_proximo_ctrl': forms.DateInput(attrs={'type': 'date'}, format="%d-%m-%Y"),
            # 'CTRL_emb_controlado',
            'CTRL_check_comienza_control_op' : forms.CheckboxInput(),
            # "Primer Trimestre (0-14 semanas)"
            'CTRL_check_pt_obstetra' : forms.CheckboxInput(),
            'CTRL_check_pt_laboratorio' : forms.CheckboxInput(),
            'CTRL_check_pt_ecografia' : forms.CheckboxInput(),
            'CTRL_check_pt_pap' : forms.CheckboxInput(),
            'CTRL_check_pt_grupofactor' : forms.CheckboxInput(),
            'CTRL_check_pt_odontologico' : forms.CheckboxInput(),
            # "Segundo Trimestre (15 a 28 semanas), 
            'CTRL_check_st_obstetra' : forms.CheckboxInput(),
            'CTRL_check_st_scanfetal' : forms.CheckboxInput(),
            'CTRL_check_st_p75' : forms.CheckboxInput(),
            # "Tercer Trimestre (29 a 41 semanas)".
            'CTRL_check_tt_obstetra' : forms.CheckboxInput(),
            'CTRL_check_tt_eco_hiso_labo' : forms.CheckboxInput(),
            'CTRL_check_tt_monitoreo_fetal' : forms.CheckboxInput(),
            'CTRL_check_tt_electrocardio' : forms.CheckboxInput(),


            # # Paso 6 : "Pareja o apoyo en la crianza" (Igual a "Padre o apoyo en la crianza, cambiar el nombre del Paso)
            # # 6.1 DATOS PERSONALES
            'POACRI_fk_pareja_apoyo_crianza': forms.Select(),
            # 'POACRI_vinculo',
            # 'POACRI_tipo_doc',
            # 'POACRI_num_doc',
            # # 6.2 EDUCACION
            # 'POACRI_edu_max_nivel',
            # 'POACRI_edu_estado',
            'POACRI_check_edu_sabe_leer': forms.CheckboxInput(),
            'POACRI_check_edu_sabe_escribir': forms.CheckboxInput(),
            'POACRI_check_edu_quiere_retomar_estudios': forms.CheckboxInput(),
            'POACRI_check_edu_quiere_aprender_oficio': forms.CheckboxInput(),
            'POACRI_check_edu_quiere_parti_prog_pilates': forms.CheckboxInput(),
            # # 6.3 ECONOMIA
            # 'POACRI_eco_planes_sociales_recibe',
            
            # # 6.4 TRABAJO
            # 'POACRI_trab_tiene_trabajo_actual',
            # 'POACRI_trab_ocupacion',
            # 'POACRI_trab_modo_contratacion',


            # # Paso 7. "Información Familiar"
            'INFOFAMI_check_convivientes_tienen_dni': forms.CheckboxInput(),
            # 'INFOFAMI_convivientes_tienen_dni_desc',
            'INFOFAMI_check_menores_escolarizados': forms.CheckboxInput(),
            # 'INFOFAMI_menores_escolarizados_desc',
            'INFOFAMI_check_menor_con_bajopes_sobrepes': forms.CheckboxInput(),
            # 'INFOFAMI_menor_con_bajopes_sobrepes_desc',
            'INFOFAMI_check_menor_con_ante_acci_dom': forms.CheckboxInput(),
            # 'INFOFAMI_menor_con_ante_acci_dom_desc',
            'INFOFAMI_check_menor_con_ante_acci_dom_seguimiento': forms.CheckboxInput(),
            'INFOFAMI_check_menores_con_ctrl_vacunas': forms.CheckboxInput(),
            # 'INFOFAMI_menores_con_ctrl_vacunas_desc',
            'INFOFAMI_check_menor_con_patologia': forms.CheckboxInput(),
            'INFOFAMI_check_menor_con_patologia_seguimiento': forms.CheckboxInput(),
            # 'INFOFAMI_menor_con_patologia_desc',
            'INFOFAMI_check_menor_capas_reduc_afec': forms.CheckboxInput(),
            # 'INFOFAMI_menor_capas_reduc_afec_desc',
            # 'INFOFAMI_conviviente_enf_infec_contagiosa',
            # 'INFOFAMI_conviviente_enf_infec_contagiosa_desc',
            'INFOFAMI_check_conviviente_consum_drogas': forms.CheckboxInput(),
            # 'INFOFAMI_conviviente_consum_drogas_desc',
            'INFOFAMI_check_emba_con_situacion_conflicto': forms.CheckboxInput(),
            'INFOFAMI_check_emba_con_situacion_conflicto_denuncio': forms.CheckboxInput(),
            'INFOFAMI_check_emba_con_situacion_conflicto_protegida': forms.CheckboxInput(),
            # 'INFOFAMI_emba_con_situacion_conflicto_desc',
            'INFOFAMI_check_familiar_con_problema_legal': forms.CheckboxInput(),
            # 'INFOFAMI_familiar_con_problema_legal_desc',
            'INFOFAMI_check_familiar_con_problema_legal_denuncio': forms.CheckboxInput(),
            'INFOFAMI_check_antecedente_duelo_trauma_reciente': forms.CheckboxInput(),
            # # Seccion 7.1. "Ingresos familiares" (dentro del paso 6)
            'INFOFAMI_ingreso_aprox': forms.NumberInput(attrs={'min': '0'}),
            'INFOFAMI_check_ingresos_plan_social': forms.CheckboxInput(),
            'INFOFAMI_check_ingreso_alcanza_alimentos': forms.CheckboxInput(),
            # 'INFOFAMI_veces_comen_aldia',

            # # Paso 8: "Acompañante y conclusiones"
            # # Sección 8.1"Conclusiones (No preguntar)"
            'CONCLUS_check_cuidador_tiene_red_proteccion': forms.CheckboxInput(),
            'CONCLUS_check_mujer_falta_valoracion': forms.CheckboxInput(),
            'CONCLUS_check_dificultad_vinculo_crianza': forms.CheckboxInput(),
            'CONCLUS_check_dificultad_compr_com': forms.CheckboxInput(),
            'CONCLUS_check_adh_sis_salud': forms.CheckboxInput(),
            'CONCLUS_check_fam_acceso_limitado_info': forms.CheckboxInput(),

            # # Sección 8.2 : Candidata a:
            'CONCLUS_check_recibir_catre': forms.CheckboxInput(),
            # 'CONCLUS_participar_de',

        }
        labels = {}

class criterios_Ingreso (forms.ModelForm):
    class Meta:
        model = Criterios_Ingreso
        fields = '__all__'
        widgets = {}
        labels = {}

class CDLE_IndiceIngresoForm (forms.ModelForm):
    class Meta:
        model = CDLE_IndiceIngreso
        fields = '__all__'
        widgets = {}
        labels = {}

class CDLE_IndiceIngresoHistorialForm (forms.ModelForm):
    class Meta:
        model = CDLE_Foto_Ingreso
        fields = '__all__'
        widgets = {}
        labels = {}


class criterios_IVI (forms.ModelForm):
    class Meta:
        model = Criterios_IVI
        fields = '__all__'
        widgets = {}
        labels = {}


class CDLE_IndiceIviForm (forms.ModelForm):
    class Meta:
        model = CDLE_IndiceIVI
        fields = '__all__'
        widgets = {}
        labels = {}

class CDLE_IndiceIviHistorialForm (forms.ModelForm):
    class Meta:
        model = CDLE_Foto_IVI
        fields = '__all__'
        widgets = {}
        labels = {}

class CDLE_IntervencionesForm (forms.ModelForm):
    class Meta:
        model = CDLE_Intervenciones
        fields = '__all__'
        widgets = {
            'detalle': forms.Textarea(attrs={'class': 'form-control','rows': 3,}),
            'responsable' : forms.SelectMultiple(attrs={'class': 'select2 w-100', 'multiple': True}),
            'fecha': forms.DateInput(attrs={'type': 'date'}, format="%Y-%m-%d"),
        }
        labels = {
            'criterio_modificable': 'Criterio modificable trabajado',
            'impacto': 'Impacto en el criterio',
            'accion': 'Acción desarrollada',
            'detalle':'Observaciones',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtra las opciones del campo criterio_modificable aquí
        self.fields['criterio_modificable'].queryset = Criterios_IVI.objects.all()

class CDLE_OpcionesResponsablesForm (forms.ModelForm):
    class Meta:
        model = OpcionesResponsables
        fields = '__all__'
        widgets = {}
        labels = {}

class CDLE_InhabilitarAdmisionEgresoForm (forms.ModelForm):
    class Meta:
        model = CDLE_Admision 
        fields = '__all__'
        widgets = {
            'check_con_control': forms.CheckboxInput(),
            'check_sin_control': forms.CheckboxInput(),
            'check_control_insuficiente': forms.CheckboxInput(),
            'check_no_aplica': forms.CheckboxInput(),
            'check_se_desconoce': forms.CheckboxInput(),
            'edad_gestacional': forms.Select(),
            'tipo_parto': forms.Select(),
            'check_internacion_en_neonatologia': forms.CheckboxInput(),
            'cuanto_tiempo': forms.Textarea(attrs={'class': 'form-control','rows': 3,}),
            'check_turno_para_cierre_hc': forms.CheckboxInput(),
        }
        labels = {}