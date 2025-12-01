from sqlmodel import Session, select
from app.models.modelos import Pedido
from app.schemas.pedido_schema import PedidoCreate, PedidoUpdate


class PedidoService:
    @staticmethod
    def get_all(db: Session):
        """Obtener todos los pedidos"""
        pedidos = db.exec(select(Pedido)).all()
        return pedidos

    @staticmethod
    def get_by_id(db: Session, pedido_id: int):
        """Obtener un pedido por ID"""
        pedido = db.get(Pedido, pedido_id)
        return pedido

    @staticmethod
    def create(db: Session, pedido: PedidoCreate):
        """Crear un nuevo pedido"""
        db_pedido = Pedido(**pedido.model_dump())
        db.add(db_pedido)
        db.commit()
        db.refresh(db_pedido)
        return db_pedido

    @staticmethod
    def update(db: Session, pedido_id: int, pedido: PedidoUpdate):
        """Actualizar un pedido existente"""
        db_pedido = db.get(Pedido, pedido_id)
        if not db_pedido:
            return None
        
        pedido_data = pedido.model_dump(exclude_unset=True)
        for key, value in pedido_data.items():
            setattr(db_pedido, key, value)
        
        db.add(db_pedido)
        db.commit()
        db.refresh(db_pedido)
        return db_pedido

    @staticmethod
    def delete(db: Session, pedido_id: int):
        """Eliminar un pedido"""
        db_pedido = db.get(Pedido, pedido_id)
        if not db_pedido:
            return None
        
        db.delete(db_pedido)
        db.commit()
        return db_pedido

    #TODO: Aqui podria ponerle chat_id en vez de usuario_id 
    # @staticmethod
    # def get_by_usuario(db: Session, usuario_id: int):
    #     """Obtener pedidos de un usuario"""
    #     pedidos = db.exec(select(Pedido).where(Pedido.usuario_id == usuario_id)).all()
    #     return pedidos

    @staticmethod
    def get_by_delivery(db: Session, delivery_id: int):
        """Obtener pedidos de un delivery"""
        pedidos = db.exec(select(Pedido).where(Pedido.delivery_id == delivery_id)).all()
        return pedidos

    @staticmethod
    def get_by_estado(db: Session, estado: str):
        """Obtener pedidos por estado"""
        pedidos = db.exec(select(Pedido).where(Pedido.estado == estado)).all()
        return pedidos
