from django.db import models
from Configuraciones.models import *
from Legajos.models import *
from django.core.validators import MinValueValidator, MaxValueValidator
from .choices import *
from django.urls import *
from SIF_CDIF.models import Criterios_IVI, OpcionesResponsables


class SL_Expedientes (models.Model):
    expediente = models.CharField(max_length=150, null=False, blank=False, verbose_name='Expediente', unique=True)
    fk_derivacion = models.ForeignKey(LegajosDerivaciones, on_delete=models.PROTECT)
    fk_equipo = models.ForeignKey(SL_Equipos, on_delete=models.PROTECT, null=True, blank=True)
    creado_por = models.ForeignKey(Usuarios, related_name='SL_Expediente_creado_por', on_delete=models.PROTECT, blank=True, null=True)
    modificado_por = models.ForeignKey(Usuarios, related_name='SL_Expediente_modificado_por', on_delete=models.PROTECT, blank=True, null=True)
    creado = models.DateField(auto_now_add=True, null=True, blank=True)
    modificado = models.DateField(auto_now=True, null=True, blank=True)
    estado = models.CharField(max_length=100, null=True, blank=True)
    derivado = models.CharField(max_length=100, default="No")

class SL_PreAdmision (models.Model):
    fk_derivacion = models.ForeignKey(LegajosDerivaciones, on_delete=models.PROTECT, null=True, blank=True)
    fk_expediente = models.ForeignKey(SL_Expedientes, on_delete=models.PROTECT)
    fk_legajo = models.ForeignKey(Legajos, on_delete=models.PROTECT, null=True, blank=True)
    

    organismo =  models.CharField(max_length=150, choices=CHOICE_TIPO_ORGANISMO, null=True, blank=True, verbose_name='Tipo de organismo')

    motivo_ingreso = models.CharField(max_length=150, choices=CHOICE_MOTIVO_INGRESO, null=True, blank=True, verbose_name='Motivo de ingreso al programa')
    obs_vulneracion = models.CharField(max_length=800, null=True, blank=True, verbose_name='Observaciones de vulneración')
    dinamica_familiar = models.CharField(max_length=800, null=True, blank=True, verbose_name='Dinamica familiar')
    conocimiento_situacion = models.CharField(max_length=150, choices=CHOICE_CONOCIMIENTO_SITUACION, null=True, blank=True, verbose_name='Como se tomó conocimiento de la situación')

    estado = models.CharField(max_length=100, null=True, blank=True)

class SL_GrupoFamiliar(models.Model):
    fk_expediente = models.ForeignKey(SL_Expedientes, on_delete=models.PROTECT)
    fk_legajo_familiar = models.ForeignKey(Legajos, on_delete=models.PROTECT, null=True, blank=True)

class SL_Alarmas(models.Model):
    fk_expediente = models.ForeignKey(SL_Expedientes, on_delete=models.PROTECT)
    fk_alarmas = models.ForeignKey(Alertas, on_delete=models.PROTECT, null=True, blank=True)

class SL_Referentes(models.Model):
    fk_expediente = models.ForeignKey(SL_Expedientes, on_delete=models.PROTECT)
    fk_legajo_referente = models.ForeignKey(Legajos, on_delete=models.PROTECT, null=True, blank=True)
    fk_externo = models.ForeignKey(AgentesExternos, on_delete=models.PROTECT, null=True, blank=True)


class SL_ExpedientesArchivos(models.Model):
    fk_expediente = models.ForeignKey(SL_Expedientes, on_delete=models.PROTECT)
    archivo = models.FileField(upload_to='ServicioLocal/archivos/', null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Archivo {self.id} del expediente {self.fk_expediente}"
    

class SL_Admision(models.Model):
    fk_expediente = models.ForeignKey(SL_Expedientes, on_delete=models.PROTECT)
    fk_preadmi = models.ForeignKey(SL_PreAdmision, on_delete=models.PROTECT) 
    estado = models.CharField(max_length=100, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

class SL_EquipoDesignado(models.Model):
    fk_equipo = models.ForeignKey(SL_Equipos, on_delete=models.PROTECT)
    fk_expediente = models.ForeignKey(SL_Expedientes, on_delete=models.PROTECT)
    fk_preadmi = models.ForeignKey(SL_PreAdmision, on_delete=models.PROTECT)
    fk_admi = models.ForeignKey(SL_Admision, on_delete=models.PROTECT)
    creado_por = models.ForeignKey(Usuarios, related_name='SL_EquipoDesignado_creado_por', on_delete=models.PROTECT, blank=True, null=True)
    modificado_por = models.ForeignKey(Usuarios, related_name='SL_EquipoDesignado_modificado_por', on_delete=models.PROTECT, blank=True, null=True)
    creado = models.DateField(auto_now_add=True, null=True, blank=True)
    modificado = models.DateField(auto_now=True, null=True, blank=True)
    
class SL_IndiceVulnerabilidad(models.Model):
    fk_indice = models.ForeignKey(SL_IndicesVulnerabilidad, on_delete=models.PROTECT, null=True, blank=True)
    fk_expediente = models.ForeignKey(SL_Expedientes, on_delete=models.PROTECT, null=True, blank=True)
    fk_preadmi = models.ForeignKey(SL_PreAdmision, on_delete=models.PROTECT, null=True, blank=True)
    creado_por = models.ForeignKey(Usuarios, related_name='SL_IndiceVulnerabilidad_creado_por', on_delete=models.PROTECT, blank=True, null=True)
    modificado_por = models.ForeignKey(Usuarios, related_name='SL_IndiceVulnerabilidad_modificado_por', on_delete=models.PROTECT, blank=True, null=True)
    creado = models.DateField(auto_now_add=True, null=True, blank=True)
    modificado = models.DateField(auto_now=True, null=True, blank=True)

class SL_Intervenciones(models.Model):
    fk_expediente = models.ForeignKey(SL_Expedientes, on_delete=models.PROTECT, null=True, blank=True)
    fk_admision = models.ForeignKey(SL_Admision, on_delete=models.PROTECT, null=True, blank=True)
    criterio_modificable = models.ForeignKey(Criterios_IVI, on_delete=models.PROTECT)
    accion = models.CharField(max_length=250, choices=CHOICE_ACCION_DESARROLLADA, null=False, blank=False)
    responsable = models.ManyToManyField(OpcionesResponsables)
    impacto = models.CharField(max_length=250, choices=[('Trabajado','Trabajado'),('Revertido','Revertido')], null=False, blank=False)
    detalle = models.CharField(max_length=350, null=True, blank=True, verbose_name='Observaciones')
    creado = models.DateField(auto_now_add=True, null=True, blank=True)
    modificado = models.DateField(auto_now=True, null=True, blank=True)
    creado_por = models.ForeignKey(Usuarios, related_name='SL_Intervenciones_creado_por', on_delete=models.PROTECT, blank=True, null=True)
    modificado_por = models.ForeignKey(Usuarios, related_name='SL_Intervenciones_modificada_por', on_delete=models.PROTECT, blank=True, null=True)



class PreadmArchivos(models.Model):

    """

    Archivos asociados a una preadmision. En la view se separaran los archivos de imagen de los documentos (para mostrar los primeros enun carousel)

    """

    fk_legajo = models.ForeignKey(Legajos, on_delete=models.PROTECT)
    archivo = models.FileField(upload_to='SIF_SL/archivos/')
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=12)
    
    def __str__(self):
        return f"Archivo {self.id} de la preadmision {self.fk_legajo}"