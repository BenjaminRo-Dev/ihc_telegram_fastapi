from sqlmodel import Session, select
from app.models.modelos import Usuario
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate


class UsuarioService:
    @staticmethod
    def get_all(db: Session):
        """Obtener todos los usuarios"""
        usuarios = db.exec(select(Usuario)).all()
        return usuarios

    @staticmethod
    def get_by_id(db: Session, usuario_id: int):
        """Obtener un usuario por ID"""
        usuario = db.get(Usuario, usuario_id)
        return usuario

    @staticmethod
    def create(db: Session, usuario: UsuarioCreate):
        """Crear un nuevo usuario"""
        db_usuario = Usuario(**usuario.model_dump())
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    @staticmethod
    def update(db: Session, usuario_id: int, usuario: UsuarioUpdate):
        """Actualizar un usuario existente"""
        db_usuario = db.get(Usuario, usuario_id)
        if not db_usuario:
            return None
        
        usuario_data = usuario.model_dump(exclude_unset=True)
        for key, value in usuario_data.items():
            setattr(db_usuario, key, value)
        
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    @staticmethod
    def delete(db: Session, usuario_id: int):
        """Eliminar un usuario"""
        db_usuario = db.get(Usuario, usuario_id)
        if not db_usuario:
            return None
        
        db.delete(db_usuario)
        db.commit()
        return db_usuario
