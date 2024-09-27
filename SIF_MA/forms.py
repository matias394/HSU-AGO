from django import forms
from .validators import MaxSizeFileValidator
from SIF_CDIF.models import Criterios_IVI
from .models import *

class MA_MultiModelForm(forms.Form):

    # Campos para SL_PreAdmision
    fk_legajo = forms.ModelChoiceField(queryset=Legajos.objects.all(), required=False)
    PER = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=True)
    juzgado = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=True)
    REUNA = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=True)
    organismo_municipal = forms.ChoiceField(choices=CHOICE_ORGANISMO_MUNICIPAL,required=False, label='Organismo municipal')
    organismo_zonal = forms.ChoiceField(choices=CHOICE_ORGANISMO_ZONAL,required=False, label='Organismo zonal')

    # Campo para SL_ExpedientesArchivos
    archivos = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    

class MA_PreadmisionesForm (forms.ModelForm):
    class Meta:
        model = MA_PreAdmision
        fields = '__all__'
        widgets = {}
        labels = {}

class MA_AdmisionForm (forms.ModelForm):
    class Meta:
        model = MA_Admision
        fields = '__all__'
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}, format="%Y-%m-%d"),
        }
        labels = {
            'fecha_ingreso':'Fecha de ingreso',
            'tipo_abrigo':'Tipo de abrigo',
            'equipo_trabajo':'Equipo de trabajo',
        }

    def clean_fecha_ingreso(self):
        fecha_ingreso = self.cleaned_data.get('fecha_ingreso')
        if not fecha_ingreso:
            raise forms.ValidationError('Este campo es obligatorio.')
        return fecha_ingreso

class MA_IntervencionesForm (forms.ModelForm):
    class Meta:
        model = MA_Intervenciones
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
        self.fields['criterio_modificable'].queryset = Criterios_IVI.objects.filter(modificable = "SI")
