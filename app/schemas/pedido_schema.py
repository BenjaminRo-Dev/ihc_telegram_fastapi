from pydantic import BaseModel


class PedidoBase(BaseModel):
    total: float
    estado: str
    ubicacion_entrega: str
    precio_delivery: float
    usuario_id: int


class PedidoCreate(PedidoBase):
    delivery_id: int | None = None


class PedidoUpdate(BaseModel):
    total: float | None = None
    estado: str | None = None
    ubicacion_entrega: str | None = None
    precio_delivery: float | None = None
    usuario_id: int | None = None
    delivery_id: int | None = None


class PedidoResponse(PedidoBase):
    id: int
    delivery_id: int | None

    class Config:
        from_attributes = True
