from django.urls import path

from .views import listar_productos, comprar_producto


urlpatterns = [

    path(
        '',
        listar_productos,
        name='listar_productos'
    ),

    path(
        'comprar/',
        comprar_producto,
        name='comprar_producto'
    ),

]