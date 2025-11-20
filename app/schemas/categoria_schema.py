from pydantic import BaseModel


class CategoriaBase(BaseModel):
    nombre: str


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(BaseModel):
    nombre: str | None = None


class CategoriaResponse(CategoriaBase):
    id: int

    class Config:
        from_attributes = True
