from sqlmodel import Session, select
from app.models.modelos import Plato
from app.schemas.plato_schema import PlatoCreate, PlatoUpdate


class PlatoService:
    @staticmethod
    def get_all(db: Session):
        """Obtener todos los platos"""
        platos = db.exec(select(Plato)).all()
        return platos

    @staticmethod
    def get_by_id(db: Session, plato_id: int):
        """Obtener un plato por ID"""
        plato = db.get(Plato, plato_id)
        return plato

    @staticmethod
    def create(db: Session, plato: PlatoCreate):
        """Crear un nuevo plato"""
        db_plato = Plato(**plato.model_dump())
        db.add(db_plato)
        db.commit()
        db.refresh(db_plato)
        return db_plato

    @staticmethod
    def update(db: Session, plato_id: int, plato: PlatoUpdate):
        """Actualizar un plato existente"""
        db_plato = db.get(Plato, plato_id)
        if not db_plato:
            return None
        
        plato_data = plato.model_dump(exclude_unset=True)
        for key, value in plato_data.items():
            setattr(db_plato, key, value)
        
        db.add(db_plato)
        db.commit()
        db.refresh(db_plato)
        return db_plato

    @staticmethod
    def delete(db: Session, plato_id: int):
        """Eliminar un plato"""
        db_plato = db.get(Plato, plato_id)
        if not db_plato:
            return None
        
        db.delete(db_plato)
        db.commit()
        return db_plato

    @staticmethod
    def get_by_categoria(db: Session, categoria_id: int):
        """Obtener platos por categoría"""
        platos = db.exec(select(Plato).where(Plato.categoria_id == categoria_id)).all()
        return platos
