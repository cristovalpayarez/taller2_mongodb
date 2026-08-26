from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.models.pedido import Pedido
from database import pedidos_collection, productos_collection


router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


@router.post("/")
async def crear_pedido(pedido: Pedido):

    # Verificar que todos los productos existan
    for item in pedido.productos:

        if not ObjectId.is_valid(item.producto_id):
            raise HTTPException(
                status_code=400,
                detail=f"ID de producto inválido: {item.producto_id}"
            )

        producto = await productos_collection.find_one(
            {"_id": ObjectId(item.producto_id)}
        )

        if producto is None:
            raise HTTPException(
                status_code=404,
                detail=f"Producto no encontrado: {item.producto_id}"
            )

        # Verificar stock
        if producto["stock"] < item.cantidad:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente para el producto: {producto['nombre']}"
            )

    # Crear el pedido
    resultado = await pedidos_collection.insert_one(
        pedido.model_dump()
    )

    # Descontar el stock
    for item in pedido.productos:

        await productos_collection.update_one(
            {"_id": ObjectId(item.producto_id)},
            {"$inc": {"stock": -item.cantidad}}
        )

    return {
        "mensaje": "Pedido creado correctamente",
        "id": str(resultado.inserted_id)
    }

@router.get("/")
async def listar_pedidos():
    pedidos = []
    # Buscamos todos los pedidos en la colección
    async for pedido in pedidos_collection.find():
        # Convertimos el _id de MongoDB (ObjectId) a string para que FastAPI pueda serializarlo a JSON
        pedido["_id"] = str(pedido["_id"])
        pedidos.append(pedido)
    return pedidos


@router.get("/{pedido_id}")
async def obtener_pedido(pedido_id: str):
    if not ObjectId.is_valid(pedido_id):
        raise HTTPException(
            status_code=400,
            detail="ID de pedido inválido"
        )

    pedido = await pedidos_collection.find_one(
        {"_id": ObjectId(pedido_id)}
    )

    if pedido is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )

    # Convertimos el ObjectId a string
    pedido["_id"] = str(pedido["_id"])
    return pedido