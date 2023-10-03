from django import forms
from .validators import MaxSizeFileValidator

from .models import *


class CDIF_PreadmisionesForm (forms.ModelForm):
    class Meta:
        model = CDIF_PreAdmisiones
        fields = '__all__'
        widgets = {
            'emb_no_control_1': forms.CheckboxInput(),
            'emb_adolescente_1': forms.CheckboxInput(),
            'emb_riesgo_1': forms.CheckboxInput(),
            'cesareas_multip_1': forms.CheckboxInput(),
            'partos_multip_1': forms.CheckboxInput(),
            'partos_premat_1': forms.CheckboxInput(),
            'partos_menos18meses_1': forms.CheckboxInput(),
            'leer_1': forms.CheckboxInput(),
            'escribir_1': forms.CheckboxInput(),
            'retomar_estudios_1': forms.CheckboxInput(),
            'aprender_oficio_1': forms.CheckboxInput(),
            'leer_2': forms.CheckboxInput(),
            'escribir_2': forms.CheckboxInput(),
            'retomar_estudios_2': forms.CheckboxInput(),
            'aprender_oficio_2': forms.CheckboxInput(),
            'programa_Pilares_2': forms.CheckboxInput(),
            'leer_3': forms.CheckboxInput(),
            'escribir_3': forms.CheckboxInput(),
            'retomar_estudios_3': forms.CheckboxInput(),
            'aprender_oficio_3': forms.CheckboxInput(),
            'programa_Pilares_3': forms.CheckboxInput(),
            'leer_4': forms.CheckboxInput(),
            'escribir_4': forms.CheckboxInput(),
            'retomar_estudios_4': forms.CheckboxInput(),
            'aprender_oficio_4': forms.CheckboxInput(),
            'programa_Pilares_4': forms.CheckboxInput(),
            'leer_5': forms.CheckboxInput(),
            'escribir_5': forms.CheckboxInput(),
            'retomar_estudios_5': forms.CheckboxInput(),
            'aprender_oficio_5': forms.CheckboxInput(),
            'programa_Pilares_5': forms.CheckboxInput(),
        }
        labels = {
            'fk_legajo_1':'',
            'vinculo_1':'',
            'tipo_doc_1':'',
            'documento_1':'',
            'menores_a_cargo_1':'',
            'control_gine_1':'',
            'embarazos_1':'',
            'abortos_esp_1':'',
            'abortos_prov_1':'',
            'hijos_1':'',
            'emb_actualmente_1':'',
            'controles_1':'',
            'emb_actual_1':'',
            'educ_maximo_1':'',
            'educ_estado_1':'',
            'planes_sociales_1':'',
            'trabajo_actual_1':'',
            'ocupacion_1':'',
            'modo_contrat_1':'',
            'fk_legajo_2':'',
            'vinculo_2':'',
            'tipo_doc_2':'',
            'documento_2':'',
            'planes_sociales_2':'',
            'trabajo_actual_2':'',
            'modo_contrat_2':'',
            'ocupacion_2':'',
            'fk_legajo_3':'',
            'vinculo_3':'',
            'tipo_doc_3':'',
            'documento_3':'',
            'fk_legajo_4':'',
            'vinculo_4':'',
            'tipo_doc_4':'',
            'documento_4':'',
            'fk_legajo_5':'',
            'vinculo_5':'',
            'tipo_doc_5':'',
            'documento_5':'',
            'centro_postula':'',
            'sala_postula':'',
            'turno_postula':'',
        }

class criterios_IVI (forms.ModelForm):
    class Meta:
        model = Criterios_IVI
        fields = '__all__'
        widgets = {}
        labels = {}

class CDIF_IndiceIviForm (forms.ModelForm):
    class Meta:
        model = CDIF_IndiceIVI
        fields = '__all__'
        widgets = {}
        labels = {}

class CDIF_IndiceIviObservForm (forms.ModelForm):
    class Meta:
        model = CDIF_IndiceIVI_Observ
        fields = '__all__'
        widgets = {}
        labels = {}