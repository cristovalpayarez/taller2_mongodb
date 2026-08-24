from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalogo.urls')),  # <-- Esto conecta las rutas de tu app catalogo con la raíz
]