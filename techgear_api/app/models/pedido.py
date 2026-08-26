from pydantic import BaseModel, Field
from typing import List


class ProductoPedido(BaseModel):
    producto_id: str
    cantidad: int = Field(..., gt=0)


class Pedido(BaseModel):
    usuario: str = Field(..., min_length=1)
    productos: List[ProductoPedido]