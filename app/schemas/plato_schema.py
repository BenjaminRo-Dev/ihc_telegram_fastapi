from pydantic import BaseModel


class PlatoBase(BaseModel):
    nombre: str
    precio_venta: float
    categoria_id: int


class PlatoCreate(PlatoBase):
    pass


class PlatoUpdate(BaseModel):
    nombre: str | None = None
    precio_venta: float | None = None
    categoria_id: int | None = None


class PlatoResponse(PlatoBase):
    id: int

    class Config:
        from_attributes = True
