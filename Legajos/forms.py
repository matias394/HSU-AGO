from django import forms
from datetime import date
from .models import *
from .validators import MaxSizeFileValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from SIF_SL.models import SL_Expedientes, SL_GrupoFamiliar, SL_PreAdmision


class LegajosForm(forms.ModelForm):
    foto = forms.ImageField(
        required=False,
        label="Foto Legajo",
        validators=[MaxSizeFileValidator(max_file_size=2)],
    )
    documento = forms.IntegerField(
        required=False,
        validators=[MinValueValidator(3000000), MaxValueValidator(100000000)],
        widget=forms.NumberInput(),
    )

    def clean(self):
        cleaned_data = super().clean()
        tipo_doc = cleaned_data.get("tipo_doc")
        documento = cleaned_data.get("documento")
        apellido = cleaned_data.get("apellido")
        nombre = cleaned_data.get("nombre")
        fecha_nacimiento = cleaned_data.get("fecha_nacimiento")

        # Validación de campo unico, combinación de DNI + Tipo DNI
        if (
            tipo_doc
            and documento
            and fecha_nacimiento
            and apellido
            and nombre
            and Legajos.objects.filter(
                tipo_doc=tipo_doc,
                documento=documento,
                apellido=apellido,
                nombre=nombre,
                fecha_nacimiento=fecha_nacimiento,
            ).exists()
        ):
            self.add_error(
                "documento", "Ya existe un legajo con ese TIPO y NÚMERO de documento."
            )
        # validación de fecha de nacimiento
        if fecha_nacimiento and fecha_nacimiento > date.today():
            self.add_error(
                "fecha_nacimiento", "La fecha de termino debe ser menor al día de hoy."
            )

        return cleaned_data

    class Meta:
        model = Legajos
        exclude = (
            "creado",
            "modificado",
        )
        widgets = {
            "fecha_nacimiento": forms.DateInput(
                attrs={"type": "date", "required": True}, format="%Y-%m-%d"
            ),
            "m2m_alertas": forms.Select(attrs={"class": "select2"}),
            "m2m_familiares": forms.Select(attrs={"class": "select2"}),
            "calle": forms.TextInput(
                attrs={"class": "form-control", "id": "calle_field"}
            ),
            "altura": forms.TextInput(
                attrs={"class": "form-control", "id": "altura_field"}
            ),
        }
        labels = {
            "nombre": "Nombre",
            "apellido": "Apellidos",
            "foto": "",
            "m2m_alertas": "",
        }


class LegajosUpdateForm(forms.ModelForm):
    foto = forms.ImageField(
        required=False,
        label="Foto Legajo",
        validators=[MaxSizeFileValidator(max_file_size=2)],
    )
    documento = forms.IntegerField(
        required=False,
        validators=[MinValueValidator(3000000), MaxValueValidator(100000000)],
        widget=forms.NumberInput(),
    )

    def clean(self):
        cleaned_data = super().clean()
        tipo_doc = cleaned_data.get("tipo_doc")
        documento = cleaned_data.get("documento")
        fecha_nacimiento = cleaned_data.get("fecha_nacimiento")
        instance = self.instance  # Obtener la instancia del objeto actual

        # Validación de campo unico, combinación de DNI + Tipo DNI
        if tipo_doc and documento:
            # Verificar si el tipo o el documento han cambiado
            if (
                tipo_doc != instance.tipo_doc or documento != instance.documento
            ) and Legajos.objects.filter(
                tipo_doc=tipo_doc, documento=documento
            ).exists():
                self.add_error(
                    "tipo", "Ya existe otro objeto con el mismo tipo y documento"
                )

        # validación de fecha de nacimiento
        if fecha_nacimiento and fecha_nacimiento > date.today():
            self.add_error(
                "fecha_nacimiento", "La fecha de termino debe ser menor al día de hoy."
            )

        return cleaned_data

    class Meta:
        model = Legajos
        exclude = ("creado", "modificado", "m2m_familiares", "m2m_alertas")
        widgets = {
            "estado": forms.Select(choices=[(True, "Activo"), (False, "Inactivo")]),
            "fecha_nacimiento": forms.DateInput(
                attrs={"type": "date"}, format="%Y-%m-%d"
            ),
        }
        labels = {
            "nombre": "Nombre",
            "apellido": "Apellidos",
            "foto": "",
        }


class LegajoGrupoFamiliarForm(forms.ModelForm):
    class Meta:
        model = LegajoGrupoFamiliar
        fields = "__all__"


class NuevoLegajoFamiliarForm(forms.ModelForm):
    vinculo = forms.ChoiceField(choices=CHOICE_VINCULO_FAMILIAR, required=True)
    estado_relacion = forms.ChoiceField(choices=CHOICE_ESTADO_RELACION, required=True)
    conviven = forms.ChoiceField(choices=CHOICE_SINO, required=True)
    cuidador_principal = forms.ChoiceField(choices=CHOICE_SINO, required=True)
    documento = forms.IntegerField(
        required=False,
        validators=[MinValueValidator(3000000), MaxValueValidator(100000000)],
        widget=forms.NumberInput(),
    )

    class Meta:
        model = Legajos
        fields = [
            "apellido",
            "nombre",
            "fecha_nacimiento",
            "tipo_doc",
            "documento",
            "sexo",
            "vinculo",
            "estado_relacion",
            "conviven",
            "cuidador_principal",
        ]
        widgets = {
            "fecha_nacimiento": forms.DateInput(
                attrs={"type": "date"}, format="%Y-%m-%d"
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo_doc = cleaned_data.get("tipo_doc")
        documento = cleaned_data.get("documento")
        fecha_nacimiento = cleaned_data.get("fecha_nacimiento")
        print(
            fecha_nacimiento > date.today(), "--------------*********-----------------"
        )

        # Validación de campo unico, combinación de DNI + Tipo DNI
        if Legajos.objects.filter(tipo_doc=tipo_doc, documento=documento).exists():
            self.add_error(
                "documento", "Ya existe un legajo con ese TIPO y NÚMERO de documento."
            )
        # validación de fecha de nacimiento
        if fecha_nacimiento and fecha_nacimiento > date.today():
            self.add_error(
                "fecha_nacimiento", "La fecha de termino debe ser menor al día de hoy."
            )

        return cleaned_data


class LegajosAlertasForm(forms.ModelForm):
    fk_categoria = forms.ModelChoiceField(
        required=True,
        label="Categoría",
        queryset=CategoriaAlertas.objects.all(),
        widget=forms.Select(attrs={"class": "select2"}),
    )

    ##borra todos los label
    # def __init__(self, *args, **kwargs):
    # super().__init__(*args, **kwargs)
    # for key, field in self.fields.items():
    # field.label = ""

    def clean(self):
        cleaned_data = super().clean()
        fk_alerta = cleaned_data.get("fk_alerta")
        fk_legajo = cleaned_data.get("fk_legajo")
        # Validación de campo unico, combinación de legajo + alerta
        if (
            fk_alerta
            and fk_legajo
            and LegajoAlertas.objects.filter(
                fk_alerta=fk_alerta, fk_legajo=fk_legajo
            ).exists()
        ):
            self.add_error("fk_alerta", "Ya existe ese alerta en el legajo")
        return cleaned_data

    class Meta:
        model = LegajoAlertas
        fields = "__all__"
        widgets = {
            "fk_alerta": forms.Select(attrs={"class": "select2"}),
        }
        labels = {"fk_alerta": "Alerta"}


class LegajosArchivosForm(forms.ModelForm):
    class Meta:
        model = LegajosArchivos
        fields = ["fk_legajo", "archivo"]


class LegajosDerivacionesForm(forms.ModelForm):
    archivos = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}), required=False
    )

    class Meta:
        model = LegajosDerivaciones
        fields = "__all__"
        exclude = ["motivo_rechazo", "obs_rechazo", "fecha_rechazo"]
        widgets = {
            "detalles": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }
        labels = {
            "fk_legajo": "Legajo",
            "fk_organismo": "Organismo desde el que se deriva",
            "m2m_alertas": "Alertas detectadas",
            "fk_programa": "Derivar a",
            "fk_programa_solicitante": "Derivar de",
            "detalles": "Motivo de la derivación o comentarios*",
        }

    def __init__(self, *args, **kwargs):
        super(LegajosDerivacionesForm, self).__init__(*args, **kwargs)

        # Obtén el valor de la opción CDIF
        cdif_value = Programas.objects.filter(
            nombre="Centros de desarrollo infanto familiar"
        ).first()

        if cdif_value:
            # Modifica el queryset del campo ForeignKey
            queryset = list(self.fields["fk_programa"].choices)

            # Agrega las opciones hardcodeadas
            opciones_adicionales = [
                (cdif_value.id, "CDIF Abriendo Alas"),
                (cdif_value.id, "CDIF Casa del Niño"),
                (cdif_value.id, "CDIF Creciendo Juntos"),
                (cdif_value.id, "CDIF Huellitas de Mitre"),
                (cdif_value.id, "CDIF La Merced"),
                (cdif_value.id, "CDIF Madre Esperanza"),
                (cdif_value.id, "CDIF Rayito de Luz"),
                (cdif_value.id, "CDIF Santa Brigida"),
                (cdif_value.id, "CDIF Semillitas del Polo"),
                (cdif_value.id, "CDIF Marilo"),
            ]

            # Combina las opciones originales y las adicionales
            todas_las_opciones = queryset + opciones_adicionales

            # Ordena alfabéticamente las opciones por la etiqueta (segundo elemento de la tupla)
            todas_las_opciones_ordenadas = sorted(
                todas_las_opciones, key=lambda x: x[1]
            )

            # Asigna las opciones ordenadas al campo
            self.fields["fk_programa"].choices = todas_las_opciones_ordenadas

    def clean(self):
        instance = super().save(commit=False)
        cleaned_data = super().clean()
        fk_programa = cleaned_data.get("fk_programa")
        fk_legajo = cleaned_data.get("fk_legajo")
        detalles = cleaned_data.get("detalles")

        if fk_programa and fk_programa.id == settings.PROG_MILD:
            if not detalles:
                self.add_error("detalles", "Este campo es obligatorio.")

        if fk_programa and fk_programa.id == settings.PROG_SL:
            archivos = self.files.get(
                "archivos"
            )  # Obtiene los archivos directamente desde self.files
            if not detalles:
                self.add_error(
                    "detalles",
                    "Este campo es obligatorio cuando el programa es Servicio Local.",
                )
                # Si existen archivos asociados, verificar si hay archivos nuevos adjuntados
            if not archivos:
                instance = self.instance
                if (
                    instance
                    and LegajosDerivacionesArchivos.objects.filter(
                        legajo_derivacion=instance
                    ).exists()
                ):
                    None
                else:
                    self.add_error("archivos", "Debe adjuntar archivo.")

        if fk_programa and fk_programa.id == settings.PROG_CDIF:
            if not detalles:
                self.add_error(
                    "detalles", "Este campo es obligatorio cuando el programa es CDIF."
                )

        if fk_programa and fk_programa.id == settings.PROG_MA:
            legajo_en_pre_admision = SL_PreAdmision.objects.filter(
                fk_derivacion__fk_legajo_id=fk_legajo.id
            ).exists()
            legajo_en_grupo_familiar = SL_GrupoFamiliar.objects.filter(
                fk_legajo_familiar_id=fk_legajo.id
            ).exists()

            if not (legajo_en_pre_admision or legajo_en_grupo_familiar):
                self.add_error(
                    "fk_programa",
                    "El legajo no se encuentra ingresado en Servicio Local.",
                )

        return cleaned_data

    def clean_archivos(self):
        archivos = self.files.getlist("archivos")
        # Puedes agregar validaciones adicionales aquí si es necesario
        return archivos

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
            for archivo in self.cleaned_data.get("archivos", []):
                LegajosDerivacionesArchivos.objects.create(
                    legajo_derivacion=instance, archivo=archivo
                )
        return instance


# Dimensiones
class DimensionFamiliaForm(forms.ModelForm):
    class Meta:
        model = DimensionFamilia
        fields = "__all__"
        widgets = {
            "obs_familia": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
            "otro_responsable": forms.Select(),
            #  'otro_responsable': forms.CheckboxInput(attrs={'class':'icheck-primary '}),
            "hay_embarazadas": forms.CheckboxInput(),
            "hay_prbl_smental": forms.CheckboxInput(),
            "hay_fam_discapacidad": forms.CheckboxInput(),
            "hay_enf_cronica": forms.CheckboxInput(),
            "hay_priv_libertad": forms.CheckboxInput(),
        }


class DimensionViviendaForm(forms.ModelForm):
    class Meta:
        model = DimensionVivienda
        fields = "__all__"
        widgets = {
            "obs_vivienda": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
            "hay_agua_caliente": forms.CheckboxInput(),
            "hay_desmoronamiento": forms.CheckboxInput(),
            "hay_banio": forms.CheckboxInput(),
        }


class DimensionSaludForm(forms.ModelForm):
    class Meta:
        model = DimensionSalud
        fields = "__all__"
        widgets = {
            "obs_salud": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
            "hay_obra_social": forms.CheckboxInput(),
            "hay_enfermedad": forms.CheckboxInput(),
            "hay_discapacidad": forms.CheckboxInput(),
            "hay_cud": forms.CheckboxInput(),
        }


class DimensionEducacionForm(forms.ModelForm):
    class Meta:
        model = DimensionEducacion
        fields = "__all__"
        widgets = {
            "obs_educacion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
            "asiste_escuela": forms.CheckboxInput(),
        }


class DimensionEconomiaForm(forms.ModelForm):
    class Meta:
        model = DimensionEconomia
        fields = "__all__"
        widgets = {
            "obs_economia": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
            "recibe_plan": forms.CheckboxInput(),
            "m2m_planes": forms.SelectMultiple(
                attrs={"class": "select2 w-100", "multiple": True}
            ),
        }
        labels = {"m2m_planes": "Planes sociales que recibe"}


class DimensionTrabajoForm(forms.ModelForm):
    class Meta:
        model = DimensionTrabajo
        fields = "__all__"
        widgets = {
            "obs_trabajo": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
            "tiene_trabajo": forms.CheckboxInput(),
            "conviviente_trabaja": forms.CheckboxInput(),
        }


class DerivacionesRechazoForm(forms.ModelForm):
    class Meta:
        model = LegajosDerivaciones
        fields = ["motivo_rechazo", "obs_rechazo", "fecha_rechazo"]
        widgets = {
            "obs_rechazo": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
        }
        labels = {
            "motivo_rechazo": "Motivo de rechazo",
            "obs_rechazo": "Observaciones",
        }
