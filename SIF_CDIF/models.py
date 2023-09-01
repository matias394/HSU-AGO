from django.db import models
from Configuraciones.models import *
from Legajos.models import *
from django.core.validators import MinValueValidator, MaxValueValidator
from .choices import *
from django.urls import *

# Create your models here.

class legajo_Programa (models.Model):
    fk_programa = models.ForeignKey(Programas, on_delete=models.PROTECT)
    fk_legajo = models.ForeignKey(Legajos, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=100, unique=True)
    estado = models.BooleanField(default=True)
    observaciones = models.CharField(max_length=300, null=True, blank=True)
    #creado_por = models.ForeignKey(Usuarios, related_name='creado_por', on_delete=models.PROTECT, blank=True, null=True)
    #modificado_por = models.ForeignKey(Usuarios, related_name='modificado_por', on_delete=models.PROTECT, blank=True, null=True)
    creado = models.DateField(auto_now_add=True)
    modificado = models.DateField(auto_now=True)

    def __str__(self):
        return self.nombre

    def clean(self):
        self.nombre = self.nombre.capitalize()

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Programa'
        verbose_name_plural = "Programas"

    def get_absolute_url(self):
        return reverse('programas_ver', kwargs={'pk': self.pk})
    
class Centros (models.Model):
    nombre = models.CharField(max_length=250, null=False, blank=False)
    sala = models.CharField(max_length=250, null=False, blank=False)
    disponibles = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.nombre

    def clean(self):
        self.nombre = self.nombre.capitalize()

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Centro'
        verbose_name_plural = "Centros"