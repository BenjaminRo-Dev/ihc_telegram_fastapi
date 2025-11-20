from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_session
from app.services.pedido_service import PedidoService
from app.schemas.pedido_schema import PedidoCreate, PedidoUpdate, PedidoResponse

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


@router.get("/", response_model=list[PedidoResponse])
def get_pedidos(db: Session = Depends(get_session)):
    """Obtener todos los pedidos"""
    return PedidoService.get_all(db)


@router.get("/usuario/{usuario_id}", response_model=list[PedidoResponse])
def get_pedidos_por_usuario(usuario_id: int, db: Session = Depends(get_session)):
    """Obtener pedidos de un usuario"""
    return PedidoService.get_by_usuario(db, usuario_id)


@router.get("/delivery/{delivery_id}", response_model=list[PedidoResponse])
def get_pedidos_por_delivery(delivery_id: int, db: Session = Depends(get_session)):
    """Obtener pedidos de un delivery"""
    return PedidoService.get_by_delivery(db, delivery_id)


@router.get("/estado/{estado}", response_model=list[PedidoResponse])
def get_pedidos_por_estado(estado: str, db: Session = Depends(get_session)):
    """Obtener pedidos por estado"""
    return PedidoService.get_by_estado(db, estado)


@router.get("/{pedido_id}", response_model=PedidoResponse)
def get_pedido(pedido_id: int, db: Session = Depends(get_session)):
    """Obtener un pedido por ID"""
    pedido = PedidoService.get_by_id(db, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido


@router.post("/", response_model=PedidoResponse, status_code=201)
def create_pedido(pedido: PedidoCreate, db: Session = Depends(get_session)):
    """Crear un nuevo pedido"""
    return PedidoService.create(db, pedido)


@router.put("/{pedido_id}", response_model=PedidoResponse)
def update_pedido(pedido_id: int, pedido: PedidoUpdate, db: Session = Depends(get_session)):
    """Actualizar un pedido existente"""
    db_pedido = PedidoService.update(db, pedido_id, pedido)
    if not db_pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return db_pedido


@router.delete("/{pedido_id}", response_model=PedidoResponse)
def delete_pedido(pedido_id: int, db: Session = Depends(get_session)):
    """Eliminar un pedido"""
    db_pedido = PedidoService.delete(db, pedido_id)
    if not db_pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return db_pedido
