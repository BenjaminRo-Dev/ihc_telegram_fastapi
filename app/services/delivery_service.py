from sqlmodel import Session, select
from app.models.modelos import Delivery
from app.schemas.delivery_schema import DeliveryCreate, DeliveryUpdate


class DeliveryService:
    @staticmethod
    def get_all(db: Session):
        """Obtener todos los deliveries"""
        deliveries = db.exec(select(Delivery)).all()
        return deliveries

    @staticmethod
    def get_by_id(db: Session, delivery_id: int):
        """Obtener un delivery por ID"""
        delivery = db.get(Delivery, delivery_id)
        return delivery

    @staticmethod
    def create(db: Session, delivery: DeliveryCreate):
        """Crear un nuevo delivery"""
        db_delivery = Delivery(**delivery.model_dump())
        db.add(db_delivery)
        db.commit()
        db.refresh(db_delivery)
        return db_delivery

    @staticmethod
    def update(db: Session, delivery_id: int, delivery: DeliveryUpdate):
        """Actualizar un delivery existente"""
        db_delivery = db.get(Delivery, delivery_id)
        if not db_delivery:
            return None
        
        delivery_data = delivery.model_dump(exclude_unset=True)
        for key, value in delivery_data.items():
            setattr(db_delivery, key, value)
        
        db.add(db_delivery)
        db.commit()
        db.refresh(db_delivery)
        return db_delivery

    @staticmethod
    def delete(db: Session, delivery_id: int):
        """Eliminar un delivery"""
        db_delivery = db.get(Delivery, delivery_id)
        if not db_delivery:
            return None
        
        db.delete(db_delivery)
        db.commit()
        return db_delivery

    @staticmethod
    def get_available(db: Session):
        """Obtener deliveries disponibles"""
        deliveries = db.exec(select(Delivery).where(Delivery.estado == True)).all()
        return deliveries
