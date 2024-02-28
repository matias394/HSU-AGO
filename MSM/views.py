from django.shortcuts import render 
from django.http import HttpResponse
import requests



def login(request):
     # URL del servicio de autenticación
    url = "https://auth-ad-srv.msm.gov.ar/api/login"

    # Datos de credenciales
    data = {
       "username": "u60901",
       "password": "!ZU$(AaH=&hdM",
    }

    # Realizar la solicitud POST
    response = requests.post(url, data=data, verify=False)

    # Verificar la respuesta
    if response.status_code == 200:
        # Credenciales válidas, obtener el token
        token = response.json().get('_token')
        
        # Guardar el token en la sesión
        request.session['_token'] = token

        # Guardar el nombre de usuario en la sesión (si está disponible)
        username = data.get('username')
        if username:
            request.session['username'] = username
        
        # Redirigir a una vista o página de éxito
        return HttpResponse(f'Token obtenido: {token} Inicio de sesión exitoso.')

    elif response.status_code == 401:
        # Credenciales inválidas
        return HttpResponse('Credenciales inválidas. No se obtuvo un token.')
    
    else:
        # Manejar otros códigos de estado según sea necesario
        return HttpResponse(f'Se recibió un código de estado inesperado: {response.status_code}')




def logout(request):
    # Obtener el token de la sesión del usuario o de donde sea que lo tengas almacenado
    token = request.session.get('_token')
    username = request.session.get('username')
    

    if not (username and token):
        return HttpResponse('Usuario no autenticado o token no válido.')

    url = "https://auth-ad-srv.msm.gov.ar/api/logout"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "username": username
    }
    response = requests.post(url, json=data, headers=headers , verify=False)
    if response.status_code == 200:

        del request.session['_token']
        del request.session['username']
        return HttpResponse("Logout Exitoso. Token eliminado.")
    else:
        return HttpResponse(f"Error: {response.status_code}")



