from pydantic import BaseModel, EmailStr


class DeliveryBase(BaseModel):
    nombre: str
    email: EmailStr


class DeliveryCreate(DeliveryBase):
    password: str


class DeliveryUpdate(BaseModel):
    nombre: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    estado: bool | None = None


class DeliveryResponse(DeliveryBase):
    id: int
    estado: bool

    class Config:
        from_attributes = True
