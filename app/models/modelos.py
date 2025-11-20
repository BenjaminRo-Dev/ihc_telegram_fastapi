from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship


class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str
    nombre: str
    username: str
    telefono: str

    pedidos: list["Pedido"] = Relationship(back_populates="usuario")


class Delivery(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    email: str
    password: str
    estado: bool = True  # disponible

    pedidos: list["Pedido"] = Relationship(back_populates="delivery")


class Categoria(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str

    platos: list["Plato"] = Relationship(back_populates="categoria")


class Plato(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    precio_venta: float

    categoria_id: int = Field(foreign_key="categoria.id")
    categoria: Categoria = Relationship(back_populates="platos")

    detalles: list["Detalle"] = Relationship(back_populates="plato")


class Pedido(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    total: float
    estado: str  # en local, en camino, entregado
    ubicacion_entrega: str
    precio_delivery: float

    usuario_id: int = Field(foreign_key="usuario.id")
    delivery_id: int | None = Field(default=None, foreign_key="delivery.id")

    usuario: Usuario = Relationship(back_populates="pedidos")
    delivery: Delivery | None = Relationship(back_populates="pedidos")

    detalles: list["Detalle"] = Relationship(back_populates="pedido")


#Tabla intermedia
class Detalle(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cantidad: int

    pedido_id: int = Field(foreign_key="pedido.id")
    plato_id: int = Field(foreign_key="plato.id")

    pedido: Pedido = Relationship(back_populates="detalles")
    plato: Plato = Relationship(back_populates="detalles")
