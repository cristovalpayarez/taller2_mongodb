from django.shortcuts import render
import requests


def listar_productos(request):

    try:
        response = requests.get("http://127.0.0.1:8000/productos/")

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


def checkout_producto(request, producto_id):

    contexto = {
        "producto_id": producto_id,
        "nombre": request.GET.get("nombre", ""),
        "precio": request.GET.get("precio", ""),
        "stock": request.GET.get("stock", ""),
    }

    return render(request, "catalogo/checkout.html", contexto)


def comprar_producto(request):

    if request.method == "POST":

        producto_id = request.POST.get("producto_id")
        cantidad = int(request.POST.get("cantidad", 1))
        usuario = request.POST.get("usuario", "").strip() or "Cliente"

        datos_pedido = {
            "usuario": usuario,
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
                mensaje = f"¡Gracias {usuario}! Tu compra se realizó correctamente."
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