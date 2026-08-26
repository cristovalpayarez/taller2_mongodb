# TechGear — Sistema Híbrido de Catálogo y Pedidos

TechGear es una tienda especializada en hardware y accesorios tecnológicos. El sistema está compuesto por dos servicios independientes que trabajan en conjunto:

- **`techgear_api`** — Microservicio construido con **FastAPI**, encargado de la lógica de negocio (catálogo de productos y gestión de pedidos), con persistencia en **MongoDB Atlas** y validación de datos mediante **Pydantic**.
- **`techgear_web`** — Portal web construido con **Django** (patrón MVT), que consume la API vía HTTP para mostrar el catálogo a los clientes y gestionar el flujo de compra (checkout).

## Arquitectura

```
taller2_mongodb/
├── techgear_api/        # Backend - API REST (FastAPI + MongoDB Atlas)
│   ├── app/
│   │   ├── models/       # Esquemas Pydantic (Producto, Pedido)
│   │   └── routes/       # Endpoints (productos, pedidos)
│   ├── database.py       # Conexión a MongoDB Atlas
│   ├── main.py           # Punto de entrada de FastAPI
│   └── requirements.txt
│
└── techgear_web/         # Frontend - Portal cliente (Django MVT)
    └── catalogo/
        ├── templates/catalogo/   # productos.html, checkout.html, resultado.html
        ├── views.py               # Consumo de la API con requests
        └── urls.py
```

## Requisitos previos

- Python 3.10 o superior
- Cuenta y cluster activo en [MongoDB Atlas](https://www.mongodb.com/atlas)
- Git

## 1. Backend — `techgear_api` (FastAPI)

### Instalación

```bash
cd techgear_api
python -m venv venv

# Activar el entorno virtual
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS / Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### Variables de entorno

Crea un archivo `.env` dentro de `techgear_api/` (este archivo **no** se sube al repositorio, está incluido en `.gitignore`):

```env
MONGO_URI=mongodb+srv://<usuario>:<password>@<tu-cluster>.mongodb.net/
MONGO_DB_NAME=techgear
```

> Reemplaza `<usuario>`, `<password>` y `<tu-cluster>` con tus credenciales reales de MongoDB Atlas. Nunca subas este archivo con las credenciales reales al repositorio.

### Ejecutar el servidor

```bash
uvicorn main:app --reload
```

- API disponible en: `http://127.0.0.1:8000`
- Documentación interactiva (Swagger UI): `http://127.0.0.1:8000/docs`

## 2. Frontend — `techgear_web` (Django)

### Instalación

```bash
cd techgear_web
python -m venv venv

# Activar el entorno virtual
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS / Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### Migraciones

```bash
python manage.py migrate
```

### Ejecutar el servidor

> **Importante:** FastAPI y Django no pueden compartir el mismo puerto. Levanta Django en un puerto distinto al 8000 (donde corre la API):

```bash
python manage.py runserver 8080
```

- Portal web disponible en: `http://127.0.0.1:8080`

## 3. Flujo de uso

Con ambos servidores corriendo simultáneamente (cada uno en su propia terminal, con su respectivo entorno virtual activado):

1. Abre `http://127.0.0.1:8080` — verás el catálogo de productos, obtenido en tiempo real desde la API de FastAPI.
2. Haz clic en **Comprar** sobre un producto disponible — te llevará a la vista de **Checkout**.
3. Completa el formulario con tu nombre y la cantidad deseada, y confirma el pedido.
4. Django envía la solicitud (POST) al endpoint `/pedidos/` de FastAPI, que valida el stock, registra el pedido en MongoDB Atlas y descuenta el inventario.
5. Verás una pantalla de confirmación con el resultado de la compra.

## Endpoints principales de la API

| Método | Endpoint          | Descripción                          |
|--------|--------------------|---------------------------------------|
| GET    | `/productos/`       | Lista todos los productos disponibles |
| POST   | `/pedidos/`         | Crea un nuevo pedido                  |
| GET    | `/pedidos/`          | Lista todos los pedidos               |
| GET    | `/pedidos/{id}`      | Consulta un pedido por su ID          |

## Notas

- El proyecto sigue control de versiones lineal, trabajando de forma secuencial sobre la rama `main`.
- Cada entrega de clase corresponde a un commit descriptivo dentro del historial del repositorio.