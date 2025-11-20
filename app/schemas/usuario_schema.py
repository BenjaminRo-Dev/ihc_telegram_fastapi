from pydantic import BaseModel


class UsuarioBase(BaseModel):
    user_id: str
    nombre: str
    username: str
    telefono: str


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioUpdate(BaseModel):
    user_id: str | None = None
    nombre: str | None = None
    username: str | None = None
    telefono: str | None = None


class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True
