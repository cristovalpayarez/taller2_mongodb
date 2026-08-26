from fastapi import APIRouter
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.models.producto import Producto
from database import productos_collection


router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)


@router.post("/")
async def crear_producto(producto: Producto):

    resultado = await productos_collection.insert_one(
        producto.model_dump()
    )

    return {
        "mensaje": "Producto creado correctamente",
        "id": str(resultado.inserted_id)
    }

@router.get("/")
async def listar_productos():

    productos = []

    cursor = productos_collection.find()

    async for producto in cursor:
        producto["id"] = str(producto["_id"])
        del producto["_id"]

        productos.append(producto)

    return productos

@router.get("/{producto_id}")
async def obtener_producto(producto_id: str):

    if not ObjectId.is_valid(producto_id):
        raise HTTPException(
            status_code=400,
            detail="ID de producto inválido"
        )

    producto = await productos_collection.find_one(
        {"_id": ObjectId(producto_id)}
    )

    if producto is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    producto["id"] = str(producto["_id"])
    del producto["_id"]

    return producto

@router.put("/{producto_id}")
async def actualizar_producto(
    producto_id: str,
    producto: Producto
):

    if not ObjectId.is_valid(producto_id):
        raise HTTPException(
            status_code=400,
            detail="ID de producto inválido"
        )

    resultado = await productos_collection.update_one(
        {"_id": ObjectId(producto_id)},
        {"$set": producto.model_dump()}
    )

    if resultado.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return {
        "mensaje": "Producto actualizado correctamente"
    }

@router.delete("/{producto_id}")
async def eliminar_producto(producto_id: str):

    if not ObjectId.is_valid(producto_id):
        raise HTTPException(
            status_code=400,
            detail="ID de producto inválido"
        )

    resultado = await productos_collection.delete_one(
        {"_id": ObjectId(producto_id)}
    )

    if resultado.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return {
        "mensaje": "Producto eliminado correctamente"
    }