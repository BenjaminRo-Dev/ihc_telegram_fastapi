from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session
from app.core.database import get_session
from app.services import telegram_service
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


@router.get("/mas-cercano", response_model=DeliveryResponse)
def get_delivery_mas_cercano(db: Session = Depends(get_session)):
    """
    Obtener el delivery disponible más cercano a la ubicación del restaurante.
    La ubicación se obtiene automáticamente de la configuración del restaurante.
    """
    try:
        delivery = DeliveryService.get_delivery_mas_cercano(db)
        if not delivery:
            raise HTTPException(status_code=404, detail="No hay deliveries disponibles")
        return delivery
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/calcular-tarifa/{ubicacion_entrega}")
def calcular_tarifa_delivery(ubicacion_entrega: str, db: Session = Depends(get_session)):
    """
    Calcular la tarifa del delivery basándose en la distancia.
    La ubicación debe estar en formato: latitud,longitud
    Ejemplo: -17.794013578375374,-63.20399069609337
    
    Retorna la tarifa calculada según: (distancia_km * precio_km) + precio_base
    """
    try:
        tarifa = DeliveryService.calcular_tarifa_delivery(db, ubicacion_entrega)
        return {"tarifa": tarifa}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


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


@router.post("/notificacion-delivery/", status_code=200)
async def notificacion_delivery(chat_id: int, nombre_delivery: str):
    print("Notificación de delivery para chat_id:", chat_id)
    msj: str = f"Salí afuera *tu pedido ya llegó!!!* \n *Delivery:* {nombre_delivery}"
    await telegram_service.enviar_mensaje(chat_id, msj)
    print("Mensaje enviado al chat_id:", chat_id)
    return JSONResponse(content= {"estado":"ok"}, status_code=200)
    