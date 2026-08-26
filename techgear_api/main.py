from fastapi import FastAPI

from app.routes.productos import router as productos_router
from app.routes.pedidos import router as pedidos_router

app = FastAPI(
    title="TechGear API",
    description="API para gestionar productos y pedidos de TechGear",
    version="1.0.0"
)


app.include_router(productos_router)
app.include_router(pedidos_router)

@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a la API de TechGear"
    }