from django import forms
from .validators import MaxSizeFileValidator
from SIF_CDIF.models import Criterios_IVI
from .models import *

class SL_MultiModelForm(forms.Form):
    # Campos para SL_Expedientes
    expediente = forms.CharField(max_length=150)
    fk_derivacion = forms.ModelChoiceField(queryset=LegajosDerivaciones.objects.all())
    fk_equipo = forms.ModelChoiceField(queryset=SL_Equipos.objects.all(), required=False)
    creado_por = forms.ModelChoiceField(queryset=Usuarios.objects.all(), required=False)
    modificado_por = forms.ModelChoiceField(queryset=Usuarios.objects.all(), required=False)
    estado = forms.CharField(max_length=100, required=False)

    # Campos para SL_PreAdmision
    fk_legajo = forms.ModelChoiceField(queryset=Legajos.objects.all(), required=False)
    organismo = forms.ChoiceField(choices=CHOICE_TIPO_ORGANISMO, required=False)
    motivo_ingreso = forms.ChoiceField(choices=CHOICE_MOTIVO_INGRESO, required=False)
    obs_vulneracion = forms.CharField(max_length=800, required=False, widget=forms.Textarea(attrs={'rows': 3}), label='Observaciones de vulneración')
    dinamica_familiar = forms.CharField(max_length=800, required=False, widget=forms.Textarea(attrs={'rows': 3}), label='Dinamica familiar')
    conocimiento_situacion = forms.ChoiceField(choices=CHOICE_CONOCIMIENTO_SITUACION, required=False)

    # Campos para SL_GrupoFamiliar
    fk_legajo_familiar = forms.ModelMultipleChoiceField(queryset=Legajos.objects.all(), required=False)

    # Campos para SL_Alarmas
    fk_alarmas = forms.ModelMultipleChoiceField(queryset=Alertas.objects.all(), required=False)

    # Campos para SL_Referentes
    fk_legajo_referente = forms.ModelMultipleChoiceField(queryset=Legajos.objects.all(), required=False)
    fk_externo = forms.ModelMultipleChoiceField(queryset=AgentesExternos.objects.all(), required=False, label="Agentes externos")

    # Campo para SL_ExpedientesArchivos
    archivos = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    def __init__(self, *args, **kwargs):
        pk_url = kwargs.pop('pk_url', None)  # Obtener el pk de la URL
        super(SL_MultiModelForm, self).__init__(*args, **kwargs)

        # Filtrar el queryset del campo fk_derivacion según el pk de la URL
        if pk_url is not None:
            self.fields['fk_derivacion'].queryset = LegajosDerivaciones.objects.filter(pk=pk_url)
    
    def clean_fk_externo(self):
        fk_externo = self.cleaned_data['fk_externo']
        if fk_externo and len(fk_externo) == 0:  # Si se proporciona una lista vacía
            raise ValidationError("Debe seleccionar al menos un agente externo.")
        return fk_externo
    
class SL_IndiceVulnerabilidadForm (forms.ModelForm):
    class Meta:
        model = SL_IndiceVulnerabilidad
        fields = '__all__'
        widgets = {}
        labels = {}


class SL_IntervencionesForm (forms.ModelForm):
    class Meta:
        model = SL_Intervenciones
        fields = '__all__'
        widgets = {
            'detalle': forms.Textarea(attrs={'class': 'form-control','rows': 3,}),
            'responsable' : forms.SelectMultiple(attrs={'class': 'select2 w-100', 'multiple': True}),
        }
        labels = {
            'criterio_modificable': 'Criterio modificable trabajado',
            'impacto': 'Impacto en el criterio',
            'accion': 'Acción desarrollada',
            'detalle':'Detalles',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtra las opciones del campo criterio_modificable aquí
        self.fields['criterio_modificable'].queryset = Criterios_IVI.objects.filter(modificable = "SI")

class SL_OpcionesResponsablesForm (forms.ModelForm):
    class Meta:
        model = OpcionesResponsables
        fields = '__all__'
        widgets = {}
        labels = {}

class PreadmArchivosForm(forms.ModelForm):
    class Meta:
        model = PreadmArchivos
        fields = ['fk_legajo', 'archivo']

class SL_EquipoDesignadoForm (forms.ModelForm):
    class Meta:
        model = SL_EquipoDesignado
        fields = '__all__'
        widgets = {}
        labels = {
            'fk_equipo':'Equipo',
        }
