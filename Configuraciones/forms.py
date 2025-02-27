from django import forms
from .models import *
from Usuarios.models import *


class SecretariasForm(forms.ModelForm):
    class Meta:
        model = Secretarias
        exclude = ()
        widgets = {
            'observaciones': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                }
            ),
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }


class SubsecretariasForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fk_secretaria'].label = "Secretaría"

    class Meta:
        model = Subsecretarias
        exclude = ()
        widgets = {
            'observaciones': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                }
            ),
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }


class ProgramasForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fk_subsecretaria'].label = "Subsecretaría"

    class Meta:
        model = Programas
        exclude = ()
        widgets = {
            'observaciones': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                }
            ),
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }


class OrganismosForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].initial = True

    class Meta:
        model = Organismos
        exclude = ()
        widgets = {
            'observaciones': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                }
            ),
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }


class PlanesSocialesForm(forms.ModelForm):
    class Meta:
        model = PlanesSociales
        exclude = ()
        widgets = {
            'observaciones': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                }
            ),
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }


class AgentesExternosForm(forms.ModelForm):
    class Meta:
        model = AgentesExternos
        exclude = ()
        labels = {
            'fk_organismo': 'Organismo',
            'telefono': 'Teléfono',
        }

        widgets = {'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')])}


class GruposDestinatariosForm(forms.ModelForm):
    class Meta:
        model = GruposDestinatarios
        exclude = ()
        widgets = {
            'm2m_usuarios': forms.SelectMultiple(
                attrs={
                    'class': 'select2 w-100',
                },
            ),
            'm2m_agentes_externos': forms.SelectMultiple(
                attrs={
                    'class': 'select2 w-100',
                },
            ),
            'observaciones': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                }
            ),
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }

        labels = {'m2m_usuarios': 'Usuarios', 'm2m_agentes_externos': 'Agentes externos'}


class CategoriaAlertasForm(forms.ModelForm):
    class Meta:
        model = CategoriaAlertas
        exclude = ()
        widgets = {
            # 'observaciones': forms.Textarea(
            #     attrs={
            #         'class': 'form-control',
            #         'rows': 3,
            #     }
            # ),
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }
        labels = {'dimension': 'Dimensión'}


class AlertasForm(forms.ModelForm):
    class Meta:
        model = Alertas
        exclude = ()
        widgets = {
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')]),
            'gravedad': forms.Select(choices=CHOICE_CRITERIO_ALERTA),
        }
        labels = {'fk_categoria': 'Categoría'}


class EquiposForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # users = users_con_permiso('programa_CDIF')
        self.fields['fk_programa'].label = "Programa"
        self.fields['m2m_usuarios'].label = "Integrantes"
        self.fields['fk_coordinador'].label = "Coordinador"
        # self.fields['m2m_usuarios'].queryset = users
        # self.fields['fk_coordinador'].initial = users

    class Meta:
        model = Equipos
        exclude = ()
        widgets = {
            'observaciones': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                }
            ),
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }


class AccionesForm(forms.ModelForm):
    class Meta:
        model = Acciones
        exclude = ()
        widgets = {
            'observaciones': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                }
            ),
        }


class CriteriosForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['m2m_acciones'].label = ""
        self.fields['m2m_alertas'].label = ""
        self.fields['fk_sujeto'].label = "Sujeto de aplicación"

    class Meta:
        model = Criterios
        exclude = ('m2m_criterios',)
        widgets = {
            'm2m_acciones': forms.SelectMultiple(
                attrs={
                    'class': 'select2 w-100',
                },
            ),
            'm2m_alertas': forms.SelectMultiple(
                attrs={
                    'class': 'select2 w-100',
                },
            ),
            'observaciones': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                }
            ),
        }


class VacantesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fk_programa'].label = "Programa"
        self.fields['fk_organismo'].label = "Organismo"
        self.fields['tipo_vacante'].label = "Tipo de vacante"
    class Meta:
        model = Vacantes
        exclude = ()
        widgets = {
            'observaciones': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                }
            ),
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')]),
            'tipo_vacante': forms.Select(choices=CHOICE_TIPO_VACANTE),
        }

class CupoVacantesForm(forms.ModelForm):

    class Meta:
        model = CupoVacante
        exclude = ('fk_vacante',)
        labels = {
            'nombre': 'Nombre del cupo',
            'cupo': 'Cupo Maximo',
            'observaciones': 'Descripcion',
        }

        widgets = {
            'observaciones': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                }
            ),
        }

        
class IndicesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['m2m_programas'].label = ""
        self.fields['nombre'].label = "Nombre del Índice"

    class Meta:
        model = Indices
        exclude = ('m2m_criterios',)
        widgets = {
            'm2m_programas': forms.SelectMultiple(
                attrs={
                    'class': 'select2 w-100',
                },
            ),
            'observaciones': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                }
            ),
        }


class IndiceCriteriosForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fk_criterio'].label = ""
        self.fields['puntaje_base'].label = ""

    class Meta:
        model = IndiceCriterios
        exclude = ('fk_indice',)


from django.forms.models import inlineformset_factory

IndicesFormset = inlineformset_factory(Indices, IndiceCriterios, form=IndiceCriteriosForm, extra=1, can_delete=True)


class SL_Equipos_Form(forms.ModelForm):
    class Meta:
        model = SL_Equipos
        exclude = ()
        widgets = {
            'observaciones': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                }
            ),
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }

class SL_IndicesVulnerabilidadForm(forms.ModelForm):
    class Meta:
        model = SL_IndicesVulnerabilidad
        exclude = ()
        widgets = {
        }
