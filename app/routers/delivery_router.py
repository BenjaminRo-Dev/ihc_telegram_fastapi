from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_session
from app.services.delivery_service import DeliveryService
from app.schemas.delivery_schema import DeliveryCreate, DeliveryUpdate, DeliveryResponse

router = APIRouter(
    prefix="/deliveries",
    tags=["Deliveries"]
)


@router.get("/", response_model=list[DeliveryResponse])
def get_deliveries(db: Session = Depends(get_session)):
    """Obtener todos los deliveries"""
    return DeliveryService.get_all(db)


@router.get("/disponibles", response_model=list[DeliveryResponse])
def get_deliveries_disponibles(db: Session = Depends(get_session)):
    """Obtener deliveries disponibles"""
    return DeliveryService.get_available(db)


@router.get("/{delivery_id}", response_model=DeliveryResponse)
def get_delivery(delivery_id: int, db: Session = Depends(get_session)):
    """Obtener un delivery por ID"""
    delivery = DeliveryService.get_by_id(db, delivery_id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery no encontrado")
    return delivery


@router.post("/", response_model=DeliveryResponse, status_code=201)
def create_delivery(delivery: DeliveryCreate, db: Session = Depends(get_session)):
    """Crear un nuevo delivery"""
    return DeliveryService.create(db, delivery)


@router.put("/{delivery_id}", response_model=DeliveryResponse)
def update_delivery(delivery_id: int, delivery: DeliveryUpdate, db: Session = Depends(get_session)):
    """Actualizar un delivery existente"""
    db_delivery = DeliveryService.update(db, delivery_id, delivery)
    if not db_delivery:
        raise HTTPException(status_code=404, detail="Delivery no encontrado")
    return db_delivery


@router.delete("/{delivery_id}", response_model=DeliveryResponse)
def delete_delivery(delivery_id: int, db: Session = Depends(get_session)):
    """Eliminar un delivery"""
    db_delivery = DeliveryService.delete(db, delivery_id)
    if not db_delivery:
        raise HTTPException(status_code=404, detail="Delivery no encontrado")
    return db_delivery
