from django.urls import path

from .views import listar_productos, checkout_producto, comprar_producto


urlpatterns = [

    path('', listar_productos, name='listar_productos'),

    path('checkout/<str:producto_id>/', checkout_producto, name='checkout'),

    path('comprar/', comprar_producto, name='comprar_producto'),

]