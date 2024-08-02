from django.db import models
from Configuraciones.models import *
from Legajos.models import *
from django.core.validators import MinValueValidator, MaxValueValidator
from .choices import *
from django.urls import *
from SIF_CDIF.models import Criterios_IVI, OpcionesResponsables
from SIF_SL.models import SL_Expedientes
from datetime import datetime
from django.utils import timezone


# Create your models here.
class MA_Derivacion (models.Model):
    fk_expediente = models.ForeignKey(SL_Expedientes, on_delete=models.PROTECT)
    creado_por = models.ForeignKey(Usuarios, related_name='MA_Derivacion_creado_por', on_delete=models.PROTECT, blank=True, null=True)
    modificado_por = models.ForeignKey(Usuarios, related_name='MA_Derivacion_modificado_por', on_delete=models.PROTECT, blank=True, null=True)
    creado = models.DateField(auto_now_add=True, null=True, blank=True)
    modificado = models.DateField(auto_now=True, null=True, blank=True)
    estado = models.CharField(max_length=100, null=True, blank=True)


class MA_PreAdmision (models.Model):
    fk_derivacion = models.ForeignKey(MA_Derivacion, on_delete=models.PROTECT)
    fk_legajo = models.ForeignKey(Legajos, related_name='MA_fk_legajo', on_delete=models.PROTECT, null=True, blank=True)
    PER = models.FileField(upload_to='MedidasAbrigo/archivos/', null=True, blank=True)
    juzgado = models.FileField(upload_to='MedidasAbrigo/archivos/', null=True, blank=True)
    REUNA = models.FileField(upload_to='MedidasAbrigo/archivos/', null=True, blank=True)
    organismo_municipal = models.CharField(max_length=250, choices=CHOICE_ORGANISMO_MUNICIPAL, null=True, blank=True)
    organismo_zonal = models.CharField(max_length=250, choices=CHOICE_ORGANISMO_ZONAL, null=True, blank=True) 

    admitido = models.CharField(max_length=150, null=True, blank=True)
    creado_por = models.ForeignKey(Usuarios, related_name='MA_PreAdm_creado_por', on_delete=models.PROTECT, blank=True, null=True)
    modificado_por = models.ForeignKey(Usuarios, related_name='MA_PreAdm_modificado_por', on_delete=models.PROTECT, blank=True, null=True)
    creado = models.DateField(auto_now_add=True, null=True, blank=True)
    modificado = models.DateField(auto_now=True, null=True, blank=True)
    estado = models.CharField(max_length=100, null=True, blank=True)
    tipo = models.CharField(max_length=100, null=True, blank=True)
    i45 = models.DateField(default=timezone.now)
    i90 = models.DateField(default=timezone.now)
    i135 = models.DateField(default=timezone.now)
    i180 = models.DateField(default=timezone.now)
    archivo45 = models.FileField(upload_to='MedidasAbrigo/archivos/', null=True, blank=True)
    archivo90 = models.FileField(upload_to='MedidasAbrigo/archivos/', null=True, blank=True)
    archivo135 = models.FileField(upload_to='MedidasAbrigo/archivos/', null=True, blank=True)
    
class MA_Familia_Abrigadora (models.Model):
    fk_preadmi = models.ForeignKey(MA_PreAdmision, on_delete=models.PROTECT)
    fk_legajo = models.ForeignKey(Legajos, related_name='MA_Familia_Abrigadora', on_delete=models.PROTECT, null=True, blank=True)

class MA_Preadmision_Archivos (models.Model):
    fk_preadmi = models.ForeignKey(MA_PreAdmision, on_delete=models.PROTECT)
    archivo = models.FileField(upload_to='MedidasAbrigo/archivos/', null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

class MA_Admision(models.Model):
    fk_preadmi = models.ForeignKey(MA_PreAdmision, on_delete=models.PROTECT)
    fecha_ingreso = models.DateField (null=True, blank=True)
    tipo_abrigo = models.CharField(max_length=150, null=True, blank=True, choices=CHOICE_TIPO_ABRIGO,)
    equipo_trabajo = models.CharField(max_length=250, null=True, blank=True, choices=CHOICE_EQUIPO_TRABAJO,)
    estado = models.CharField(max_length=150, null=True, blank=True, default="Activa")
    creado = models.DateField(auto_now_add=True, null=True, blank=True)
    modificado = models.DateField(auto_now=True, null=True, blank=True)
    creado_por = models.ForeignKey(Usuarios, related_name='MA_Admision_creado_por', on_delete=models.PROTECT, blank=True, null=True)
    modificado_por = models.ForeignKey(Usuarios, related_name='MA_Admision_modificada_por', on_delete=models.PROTECT, blank=True, null=True)

class MA_Expedientes_Archivos (models.Model):
    fk_derivacion = models.ForeignKey(MA_Derivacion, on_delete=models.PROTECT)
    archivo = models.FileField(upload_to='MedidasAbrigo/archivos/', null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

class MA_Intervenciones(models.Model):
    fk_admision = models.ForeignKey(MA_Admision, on_delete=models.PROTECT, null=True, blank=True)
    criterio_modificable = models.ForeignKey(Criterios_IVI, on_delete=models.PROTECT)
    accion = models.CharField(max_length=250, choices=CHOICE_ACCION_DESARROLLADA, null=False, blank=False)
    responsable = models.ManyToManyField(OpcionesResponsables)
    impacto = models.CharField(max_length=250, choices=[('Trabajado','Trabajado'),('Revertido','Revertido')], null=False, blank=False)
    detalle = models.CharField(max_length=350, null=True, blank=True, verbose_name='Observaciones')
    creado = models.DateField(auto_now_add=True, null=True, blank=True)
    modificado = models.DateField(auto_now=True, null=True, blank=True)
    creado_por = models.ForeignKey(Usuarios, related_name='MA_Intervenciones_creado_por', on_delete=models.PROTECT, blank=True, null=True)
    modificado_por = models.ForeignKey(Usuarios, related_name='MA_Intervenciones_modificada_por', on_delete=models.PROTECT, blank=True, null=True)

