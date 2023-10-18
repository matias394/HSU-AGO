from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import FormView ,DetailView ,CreateView ,UpdateView ,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from Legajos.models import *
from Configuraciones.models import *
from datetime import date, timedelta


class BusquedaMenu(LoginRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        menu = self.request.GET.get('punto_menu')
        puntos = [
            'dashboard',
            'secretarías',
            'secretarias',
            'subsecretarías',
            'subsecretarias',
            'programas',
            'organismos',
            'planes sociales',
            'agentes externos',
            'grupos de destinatarios',
            'tipos de alertas',
            'equipos',
            'acciones',
            'criterios',
            'índices',
            'indices',
            'usuarios',
            'grupos de usuario',
            'legajos',
            'derivaciones',
            'admisiones',
            'intervenciones',
        ]
        if menu and (menu.lower() in puntos):
            menu = menu.lower()
            if menu == "dashboard":
                return redirect('dashboard_listar')
            elif menu == 'secretarías' or menu == 'secretarias':
                return redirect('secretarias_listar')
            elif menu == 'subsecretarías' or menu == 'subsecretarias':
                return redirect('subsecretarias_listar')
            elif menu == 'programas':
                return redirect('programas_listar')
            elif menu == 'organismos':
                return redirect('organismos_listar')
            elif menu == 'equipos':
                return redirect('equipos_listar')
            elif menu == 'acciones':
                return redirect('acciones_listar')
            elif menu == 'criterios':
                return redirect('criterios_listar')
            elif menu == 'índices' or menu == 'indices':
                return redirect('índices_listar')
            elif menu == 'usuarios':
                return redirect('usuarios_listar')
            elif menu == 'legajos':
                return redirect('legajos_listar')
            elif menu == 'derivaciones':
                return redirect('legajosderivaciones_listar')
            elif menu == 'admisiones':
                return redirect('preadmisiones_listar')
            elif menu == 'intervenciones':
                return redirect('intervenciones_legajolistar')
            elif menu == 'planes sociales':
                return redirect('planes_sociales_listar')
            elif menu == 'agentes externos':
                return redirect('agentesexternos_listar')
            elif menu == 'grupos de usuario':
                return redirect('grupos_listar')
            elif menu == 'grupos de destinatarios':
                return redirect('gruposdestinatarios_listar')
            elif menu == 'categorias de alertas':
                return redirect('categoriaalertas_listar')
            elif menu == 'alertas':
                return redirect('alertas_listar')
        else:
            messages.error(self.request, ('No existen resultados.'))
            return redirect('legajos_listar')
        
def contar_legajos():
    # Cuenta la cantidad total de legajos
    cantidad_total_legajos = Legajos.objects.count()

    # Realiza el cálculo de la cantidad de legajos activos
    legajos_activos = Legajos.objects.filter(estado=True)
    cantidad_legajos_activos = legajos_activos.count()
    
    return  cantidad_total_legajos,cantidad_legajos_activos

def contar_legajos_entre_0_y_18_anios():
    # Obtiene la fecha actual
    today = date.today()

    # Calcula la fecha de hace 18 años
    fecha_hace_18_anios = today - timedelta(days=18 * 365)

    # Realiza una consulta para contar los legajos que tienen entre 0 y 18 años
    cantidad_legajos = Legajos.objects.filter(fecha_nacimiento__gte=fecha_hace_18_anios).count()
    return cantidad_legajos


def contar_alarmas_activas():
    # Realiza el cálculo de la cantidad de legajos activos
    alarmas_activas = Alertas.objects.filter(gravedad='Critica')
    cantidad_alarmas_activas = alarmas_activas.count()
    
    return cantidad_alarmas_activas

def contar_legajos_con_planes_sociales():
    # Utiliza una subconsulta para contar los Legajos con planes sociales a través de DimensionEconomia
    cantidad = Legajos.objects.filter(dimensioneconomia__m2m_planes__isnull=False).distinct().count()
    return cantidad


    
        

class DashboardView(TemplateView):
    template_name = "dashboard.html"
    queryset = Legajos.objects.filter(estado=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtén las cantidades de legajos
        cantidad_total_legajos, cantidad_legajos_activos  = contar_legajos()
        cantidad_legajos_entre_0_y_18_anios = contar_legajos_entre_0_y_18_anios()

        # Agrega las cantidades al contexto
        context['cantidad_legajos'] = cantidad_legajos_entre_0_y_18_anios
        context['cantidad_total_legajos'] = cantidad_total_legajos
        context['cantidad_legajos_activos'] = cantidad_legajos_activos

         # Filtrar las alertas con gravedad "Critica" y estado "alarmas_activas"
        cantidad_alarmas_activas = Alertas.objects.filter(gravedad='Critica').count()

        # Agrega la cantidad de alarmas activas al contexto
        context['cantidad_alarmas_activas'] = cantidad_alarmas_activas

        # Obtén la cantidad de legajos con planes sociales utilizando la función
        cantidad_legajos_con_planes_sociales = contar_legajos_con_planes_sociales()

        # Agrega la cantidad al contexto
        context['cantidad_legajos_con_planes_sociales'] = cantidad_legajos_con_planes_sociales

        return context
    

        


