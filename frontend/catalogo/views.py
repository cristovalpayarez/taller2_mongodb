from django.shortcuts import render
import requests

def listar_productos(request):
    try:
        # Hacemos una petición GET a la API de FastAPI que hicimos en la Clase 2
        response = requests.get("http://127.0.0.1:8000/productos/")
        
        # Si la petición es exitosa (código 200)
        if response.status_code == 200:
            productos = response.json()
        else:
            productos = []
    except requests.exceptions.ConnectionError:
        # Si FastAPI está apagado o no se puede conectar
        productos = []

    # Enviamos los productos a la plantilla HTML que crearemos en el siguiente paso
    return render(request, 'catalogo/productos.html', {"productos": productos})