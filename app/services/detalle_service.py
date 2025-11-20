from sqlmodel import Session, select
from app.models.modelos import Detalle
from app.schemas.detalle_schema import DetalleCreate, DetalleUpdate


class DetalleService:
    @staticmethod
    def get_all(db: Session):
        """Obtener todos los detalles"""
        detalles = db.exec(select(Detalle)).all()
        return detalles

    @staticmethod
    def get_by_id(db: Session, detalle_id: int):
        """Obtener un detalle por ID"""
        detalle = db.get(Detalle, detalle_id)
        return detalle

    @staticmethod
    def create(db: Session, detalle: DetalleCreate):
        """Crear un nuevo detalle"""
        db_detalle = Detalle(**detalle.model_dump())
        db.add(db_detalle)
        db.commit()
        db.refresh(db_detalle)
        return db_detalle

    @staticmethod
    def update(db: Session, detalle_id: int, detalle: DetalleUpdate):
        """Actualizar un detalle existente"""
        db_detalle = db.get(Detalle, detalle_id)
        if not db_detalle:
            return None
        
        detalle_data = detalle.model_dump(exclude_unset=True)
        for key, value in detalle_data.items():
            setattr(db_detalle, key, value)
        
        db.add(db_detalle)
        db.commit()
        db.refresh(db_detalle)
        return db_detalle

    @staticmethod
    def delete(db: Session, detalle_id: int):
        """Eliminar un detalle"""
        db_detalle = db.get(Detalle, detalle_id)
        if not db_detalle:
            return None
        
        db.delete(db_detalle)
        db.commit()
        return db_detalle

    @staticmethod
    def get_by_pedido(db: Session, pedido_id: int):
        """Obtener detalles de un pedido"""
        detalles = db.exec(select(Detalle).where(Detalle.pedido_id == pedido_id)).all()
        return detalles
