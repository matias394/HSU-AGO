from django.db import models
from Configuraciones.models import *
from Legajos.models import *
from django.core.validators import MinValueValidator, MaxValueValidator
from .choices import *
from django.urls import *

# Create your models here.

#class legajo_CDIF (models.Model):
#    fk_programa = models.ForeignKey(Programas, on_delete=models.PROTECT)
#    fk_legajo = models.ForeignKey(Legajos, on_delete=models.PROTECT)
#    nombre = models.CharField(max_length=100, unique=True)
#    estado = models.BooleanField(default=True)
#    observaciones = models.CharField(max_length=300, null=True, blank=True)
#    #creado_por = models.ForeignKey(Usuarios, related_name='creado_por', on_delete=models.PROTECT, blank=True, null=True)
#    #modificado_por = models.ForeignKey(Usuarios, related_name='modificado_por', on_delete=models.PROTECT, blank=True, null=True)
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

class CDIF_PreAdmision (models.Model):
    fk_derivacion = models.ForeignKey(LegajosDerivaciones, on_delete=models.PROTECT)
    fk_legajo = models.ForeignKey(Legajos, related_name='fk_legajo', on_delete=models.PROTECT, null=True, blank=True)
    fk_legajo_1 = models.ForeignKey(Legajos, related_name='fk_legajo_1', on_delete=models.PROTECT, null=True, blank=True)
    fk_legajo_2 = models.ForeignKey(Legajos, related_name='fk_legajo_2', on_delete=models.PROTECT, null=True, blank=True)
    menores_a_cargo_1 = models.CharField(max_length=50, choices=CHOICE_1A5, null=True, blank=True)
    control_gine_1 =  models.CharField(max_length=50, choices=CHOICE_SINO, null=True, blank=True)
    hijos_1 = models.CharField(max_length=50, choices=CHOICE_1A5, null=True, blank=True)
    embarazos_1 = models.CharField(max_length=50, choices=CHOICE_1A5, null=True, blank=True)
    abortos_esp_1 = models.CharField(max_length=50, choices=CHOICE_1A5, null=True, blank=True)
    abortos_prov_1 = models.CharField(max_length=50, choices=CHOICE_1A5, null=True, blank=True)
    emb_no_control_1 = models.BooleanField(verbose_name='Embarazo NO controlado', null=True, blank=True)
    emb_adolescente_1 = models.BooleanField(verbose_name='Embarazo adolescente', null=True, blank=True)
    emb_riesgo_1 = models.BooleanField(verbose_name='Embarazo de riesgo', null=True, blank=True)
    cesareas_multip_1 = models.BooleanField(verbose_name='Cesáreas múltiples', null=True, blank=True)
    partos_multip_1 = models.BooleanField(verbose_name='Partos múltiples', null=True, blank=True)
    partos_premat_1 = models.BooleanField(verbose_name='Partos prematuros', null=True, blank=True)
    partos_menos18meses_1 = models.BooleanField(verbose_name='Partos con menos de 18 meses de intervalo', null=True, blank=True)
    emb_actualmente_1 =  models.CharField(max_length=50, choices=CHOICE_SINO, null=True, blank=True)
    controles_1 =  models.CharField(max_length=50, choices=CHOICE_SINO, null=True, blank=True)
    emb_actual_1 =  models.CharField(max_length=150, choices=CHOICE_EMB_RIESGO, null=True, blank=True)
    educ_maximo_1 =  models.CharField(max_length=150, choices=CHOICE_EDUCACION, null=True, blank=True)
    educ_estado_1 =  models.CharField(max_length=150, choices=CHOICE_ESTADO, null=True, blank=True)
    leer_1 = models.BooleanField(verbose_name='No sabe leer', null=True, blank=True)
    escribir_1 = models.BooleanField(verbose_name='No sabe escribir', null=True, blank=True)
    retomar_estudios_1 = models.BooleanField(verbose_name='Quiere retomar estudios', null=True, blank=True)
    aprender_oficio_1 = models.BooleanField(verbose_name='Quiere aprender un oficio', null=True, blank=True)
    planes_sociales_1 = models.ManyToManyField(PlanesSociales, related_name='planes_sociales_1',null=True, blank=True)
    trabajo_actual_1 =  models.CharField(max_length=50, choices=CHOICE_SINO, null=True, blank=True)
    ocupacion_1 = models.CharField(verbose_name='Ocupación', max_length=100, null=True, blank=True)
    modo_contrat_1 =  models.CharField(max_length=150, choices=CHOICE_CONTRATACION, null=True, blank=True)
    educ_maximo_2 =  models.CharField(max_length=150, choices=CHOICE_EDUCACION, null=True, blank=True)
    educ_estado_2 =  models.CharField(max_length=150, choices=CHOICE_ESTADO, null=True, blank=True)
    leer_2 = models.BooleanField(verbose_name='No sabe leer', null=True, blank=True)
    escribir_2 = models.BooleanField(verbose_name='No sabe escribir', null=True, blank=True)
    retomar_estudios_2 = models.BooleanField(verbose_name='Quiere retomar estudios', null=True, blank=True)
    aprender_oficio_2 = models.BooleanField(verbose_name='Quiere aprender un oficio', null=True, blank=True)
    programa_Pilares_2 = models.BooleanField(verbose_name='Quiere participar del Programa Pilares', null=True, blank=True)
    planes_sociales_2 = models.ManyToManyField(PlanesSociales, related_name='planes_sociales_2',null=True, blank=True)
    trabajo_actual_2 =  models.CharField(max_length=50, choices=CHOICE_SINO, null=True, blank=True)
    ocupacion_2 = models.CharField(verbose_name='Ocupación', max_length=100, null=True, blank=True)
    modo_contrat_2 =  models.CharField(max_length=150, choices=CHOICE_CONTRATACION, null=True, blank=True)
    fk_legajo_3 = models.ForeignKey(Legajos, related_name='fk_legajo_3', on_delete=models.PROTECT, null=True, blank=True)
    educ_maximo_3 =  models.CharField(max_length=150, choices=CHOICE_EDUCACION, null=True, blank=True)
    educ_estado_3 =  models.CharField(max_length=150, choices=CHOICE_ESTADO, null=True, blank=True)
    leer_3 = models.BooleanField(verbose_name='No sabe leer', null=True, blank=True)
    escribir_3 = models.BooleanField(verbose_name='No sabe escribir', null=True, blank=True)
    retomar_estudios_3 = models.BooleanField(verbose_name='Quiere retomar estudios', null=True, blank=True)
    aprender_oficio_3 = models.BooleanField(verbose_name='Quiere aprender un oficio', null=True, blank=True)
    programa_Pilares_3 = models.BooleanField(verbose_name='Quiere participar del Programa Pilares', null=True, blank=True)
    fk_legajo_4 = models.ForeignKey(Legajos, related_name='fk_legajo_4', on_delete=models.PROTECT, null=True, blank=True)
    educ_maximo_4 =  models.CharField(max_length=150, choices=CHOICE_EDUCACION, null=True, blank=True)
    educ_estado_4 =  models.CharField(max_length=150, choices=CHOICE_ESTADO, null=True, blank=True)
    leer_4 = models.BooleanField(verbose_name='No sabe leer', null=True, blank=True)
    escribir_4 = models.BooleanField(verbose_name='No sabe escribir', null=True, blank=True)
    retomar_estudios_4 = models.BooleanField(verbose_name='Quiere retomar estudios', null=True, blank=True)
    aprender_oficio_4 = models.BooleanField(verbose_name='Quiere aprender un oficio', null=True, blank=True)
    programa_Pilares_4 = models.BooleanField(verbose_name='Quiere participar del Programa Pilares', null=True, blank=True)
    fk_legajo_5 = models.ForeignKey(Legajos, related_name='fk_legajo_5', on_delete=models.PROTECT, null=True, blank=True)
    educ_maximo_5 =  models.CharField(max_length=150, choices=CHOICE_EDUCACION, null=True, blank=True)
    educ_estado_5 =  models.CharField(max_length=150, choices=CHOICE_ESTADO, null=True, blank=True)
    leer_5 = models.BooleanField(verbose_name='No sabe leer', null=True, blank=True)
    escribir_5 = models.BooleanField(verbose_name='No sabe escribir', null=True, blank=True)
    retomar_estudios_5 = models.BooleanField(verbose_name='Quiere retomar estudios', null=True, blank=True)
    aprender_oficio_5 = models.BooleanField(verbose_name='Quiere aprender un oficio', null=True, blank=True)
    programa_Pilares_5 = models.BooleanField(verbose_name='Quiere participar del Programa Pilares', null=True, blank=True)
    centro_postula = models.ForeignKey(Vacantes, on_delete=models.PROTECT, null=False, blank=False)
    sala_postula = models.ForeignKey(CupoVacante, on_delete=models.PROTECT, null=False, blank=False)
    #turno_postula =  models.CharField(max_length=150, choices=CHOICE_TURNO_POSTULA, null=False, blank=False)
    sala_short = models.CharField(max_length=150, null=True, blank=True)
    vinculo1 = models.CharField(max_length=150, null=True, blank=True)
    vinculo2 = models.CharField(max_length=150, null=True, blank=True)
    vinculo3 = models.CharField(max_length=150, null=True, blank=True)
    vinculo4 = models.CharField(max_length=150, null=True, blank=True)
    vinculo5 = models.CharField(max_length=150, null=True, blank=True)
    ivi = models.CharField(max_length=150, null=True, blank=True)
    admitido = models.CharField(max_length=150, null=True, blank=True)
    creado_por = models.ForeignKey(Usuarios, related_name='PreAdm_creado_por', on_delete=models.PROTECT, blank=True, null=True)
    modificado_por = models.ForeignKey(Usuarios, related_name='PreAdm_modificado_por', on_delete=models.PROTECT, blank=True, null=True)
    creado = models.DateField(auto_now_add=True, null=True, blank=True)
    modificado = models.DateField(auto_now=True, null=True, blank=True)
    estado = models.CharField(max_length=100, null=True, blank=True)
    tipo = models.CharField(max_length=100, null=True, blank=True)
    observaciones = models.CharField(max_length=300, null=True, blank=True)

class Criterios_IVI(models.Model):
    criterio =  models.CharField(max_length=250, null=False, blank=False)
    tipo =  models.CharField(max_length=250, choices=CHOICE_TIPO_IVI, null=False, blank=False)
    puntaje =  models.SmallIntegerField(null=False, blank=False)
    modificable =  models.CharField(max_length=50, choices=CHOICE_NOSI_MODIFICABLE, null=False, blank=False)
    
    def __str__(self):
        return self.criterio

class CDIF_IndiceIVI(models.Model):
    fk_criterios_ivi = models.ForeignKey(Criterios_IVI, on_delete=models.PROTECT)
    fk_legajo = models.ForeignKey(Legajos, on_delete=models.PROTECT, null=True, blank=True)
    fk_preadmi = models.ForeignKey(CDIF_PreAdmision, on_delete=models.PROTECT, null=True, blank=True)
    presencia = models.BooleanField (default=False, null=True, blank=True)
    tipo = models.CharField (max_length=350, null=True, blank=True)
    programa = models.CharField(max_length=150, choices=CHOICE_NOSI_MODIFICABLE, null=True, blank=True)
    clave = models.CharField (max_length=350, null=True, blank=True)
    creado = models.DateField(auto_now_add=True, null=True, blank=True)
    modificado = models.DateField(auto_now=True, null=True, blank=True)

class CDIF_Foto_IVI(models.Model):
    fk_preadmi = models.ForeignKey(CDIF_PreAdmision, on_delete=models.PROTECT, null=True, blank=True)
    fk_legajo = models.ForeignKey(Legajos, on_delete=models.PROTECT, null=True, blank=True)
    puntaje = models.SmallIntegerField(null=True, blank=True) 
    puntaje_max = models.SmallIntegerField(null=True, blank=True)
    crit_modificables = models.SmallIntegerField(null=True, blank=True)
    crit_presentes = models.SmallIntegerField(null=True, blank=True)
    observaciones = models.CharField(max_length=350, null=True, blank=True)
    tipo = models.CharField (max_length=350, null=True, blank=True)
    clave = models.CharField (max_length=350, null=True, blank=True)
    creado_por = models.ForeignKey(Usuarios, related_name='IVI_creado_por', on_delete=models.PROTECT, blank=True, null=True)
    modificado_por = models.ForeignKey(Usuarios, related_name='IVI_modificado_por', on_delete=models.PROTECT, blank=True, null=True)
    creado = models.DateField(auto_now_add=True, null=True, blank=True)
    modificado = models.DateField(auto_now=True, null=True, blank=True)
 
class CDIF_Vacantes(models.Model):
    fk_legajo = models.ForeignKey(Legajos, on_delete=models.PROTECT, null=True, blank=True)
    fk_derivacion = models.ForeignKey(CDIF_PreAdmision, on_delete=models.PROTECT, null=True, blank=True)
    fk_vacantes = models.ForeignKey(Vacantes, on_delete=models.PROTECT, null=True, blank=True)
    organizacion = models.CharField(max_length=100)
    fk_organismo = models.ForeignKey(Organismos, on_delete=models.PROTECT, null=True, blank=True)  # Nueva línea
    sala = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    creado = models.DateField(auto_now_add=True, null=True, blank=True)
    modificado = models.DateField(auto_now=True, null=True, blank=True)
    creado_por = models.ForeignKey(Usuarios, related_name='Vacante_creado_por', on_delete=models.PROTECT, blank=True, null=True)
    modificado_por = models.ForeignKey(Usuarios, related_name='Vacante_modificada_por', on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return f'{self.organizacion} - Sala {self.sala}'


class CDIF_Admision(models.Model):
    fk_preadmi = models.ForeignKey(CDIF_PreAdmision, on_delete=models.PROTECT)
    estado_vacante = models.CharField(max_length=150, null=True, blank=True)
    estado = models.CharField(max_length=150, null=True, blank=True, default="Activa")
    creado = models.DateField(auto_now_add=True, null=True, blank=True)
    modificado = models.DateField(auto_now=True, null=True, blank=True)
    creado_por = models.ForeignKey(Usuarios, related_name='Admision_creado_por', on_delete=models.PROTECT, blank=True, null=True)
    modificado_por = models.ForeignKey(Usuarios, related_name='Admision_modificada_por', on_delete=models.PROTECT, blank=True, null=True)
    inactiva_observaciones = models.CharField(max_length=300, null=True, blank=True)
    inactiva_tipo_baja = models.CharField(max_length=100, null=True, blank=True)
    inactiva_motivo_baja = models.CharField(max_length=100, null=True, blank=True) 

class CDIF_VacantesOtorgadas (models.Model):
    fk_admision = models.ForeignKey(CDIF_Admision, on_delete=models.PROTECT)
    fk_organismo = models.ForeignKey(Vacantes, on_delete=models.PROTECT)
    sala = models.ForeignKey(CupoVacante, on_delete=models.PROTECT, null=False, blank=False)
    educador = models.CharField(max_length=150, null=True, blank=True)
    estado_vacante = models.CharField(max_length=150, null=True, blank=True, default="Asignada")
    fecha_ingreso = models.DateField(null=False, blank=False)
    fecha_egreso = models.DateField(null=True, blank=True)
    motivo = models.CharField(max_length=100, null=True, blank=True)
    detalles = models.CharField(max_length=350, null=True, blank=True)
    evento = models.CharField(max_length=100, null=True, blank=True)
    creado = models.DateField(auto_now_add=True, null=True, blank=True)
    modificado = models.DateField(auto_now=True, null=True, blank=True)
    creado_por = models.ForeignKey(Usuarios, related_name='VacanteOtorgada_creado_por', on_delete=models.PROTECT, blank=True, null=True)
    modificado_por = models.ForeignKey(Usuarios, related_name='VacanteOtorgada_modificada_por', on_delete=models.PROTECT, blank=True, null=True)


class CDIF_HistorialVacantes (models.Model):
    fk_admision = models.ForeignKey(CDIF_Admision, on_delete=models.PROTECT)
    fk_organismo = models.ForeignKey(Vacantes, on_delete=models.PROTECT)
    estado = models.CharField(max_length=150, null=True, blank=True)
    sala = models.CharField(max_length=150, null=True, blank=True)
    creado = models.DateField(auto_now_add=True, null=True, blank=True)
    modificado = models.DateField(auto_now=True, null=True, blank=True)
    creado_por = models.ForeignKey(Usuarios, related_name='HistorialVacantes_creado_por', on_delete=models.PROTECT, blank=True, null=True)
    modificado_por = models.ForeignKey(Usuarios, related_name='HistorialVacantes_modificada_por', on_delete=models.PROTECT, blank=True, null=True)

class OpcionesResponsables(models.Model):
    nombre = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.nombre

class CDIF_Intervenciones(models.Model):
    fk_admision = models.ForeignKey(CDIF_Admision, on_delete=models.PROTECT, null=True, blank=True)
    criterio_modificable = models.ForeignKey(Criterios_IVI, on_delete=models.PROTECT)
    accion = models.CharField(max_length=250, choices=CHOICE_ACCION_DESARROLLADA, null=False, blank=False)
    responsable = models.ManyToManyField(OpcionesResponsables)
    impacto = models.CharField(max_length=250, choices=[('Trabajado','Trabajado'),('Revertido','Revertido')], null=False, blank=False)
    detalle = models.CharField(max_length=350, null=True, blank=True, verbose_name='Observaciones')
    creado = models.DateField(auto_now_add=True, null=True, blank=True)
    modificado = models.DateField(auto_now=True, null=True, blank=True)
    creado_por = models.ForeignKey(Usuarios, related_name='Intervenciones_creado_por', on_delete=models.PROTECT, blank=True, null=True)
    modificado_por = models.ForeignKey(Usuarios, related_name='Intervenciones_modificada_por', on_delete=models.PROTECT, blank=True, null=True)
    fecha = models.DateField(null=True, blank=True)


class CDIF_Historial(models.Model):
    fk_legajo = models.ForeignKey(Legajos, on_delete=models.PROTECT, null=True, blank=True)
    fk_legajo_derivacion = models.ForeignKey(LegajosDerivaciones, on_delete=models.PROTECT, null=True, blank=True)
    fk_preadmi = models.ForeignKey(CDIF_PreAdmision, on_delete=models.PROTECT, null=True, blank=True)
    fk_admision = models.ForeignKey(CDIF_Admision, on_delete=models.PROTECT, null=True, blank=True)
    movimiento = models.CharField(max_length=150, null=True, blank=True)
    creado = models.DateField(auto_now_add=True, null=True, blank=True)
    creado_por = models.ForeignKey(Usuarios, on_delete=models.PROTECT, null=True, blank=True)

