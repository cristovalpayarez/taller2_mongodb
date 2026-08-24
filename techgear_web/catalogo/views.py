from django.shortcuts import render
import requests


def listar_productos(request):

    try:

        response = requests.get(
            "http://127.0.0.1:8000/productos/"
        )

        if response.status_code == 200:
            productos = response.json()
        else:
            productos = []

    except requests.exceptions.ConnectionError:

        productos = []

    return render(
        request,
        'catalogo/productos.html',
        {"productos": productos}
    )


def comprar_producto(request):

    if request.method == "POST":

        producto_id = request.POST.get("producto_id")
        cantidad = int(request.POST.get("cantidad", 1))

        datos_pedido = {
            "usuario": "Cliente",
            "productos": [
                {
                    "producto_id": producto_id,
                    "cantidad": cantidad
                }
            ]
        }

        try:

            response = requests.post(
                "http://127.0.0.1:8000/pedidos/",
                json=datos_pedido
            )

            if response.status_code == 200:

                mensaje = "¡Compra realizada correctamente!"

            else:

                mensaje = response.json().get(
                    "detail",
                    "No se pudo realizar la compra."
                )

        except requests.exceptions.ConnectionError:

            mensaje = "No se pudo conectar con la API."

    else:

        mensaje = "Método no permitido."

    return render(
        request,
        "catalogo/resultado.html",
        {"mensaje": mensaje}
    )