from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView,TemplateView
from Legajos.models import LegajosDerivaciones
from django.db.models import Q
# # Create your views here.
# derivaciones = LegajosDerivaciones.objects.filter(m2m_programas__nombr__iexact="CDIF")
# print(derivaciones)

