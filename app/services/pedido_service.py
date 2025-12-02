from sqlmodel import Session, select
from app.models.modelos import Pedido, Detalle
from app.schemas.pedido_schema import PedidoCreate, PedidoUpdate, PedidoCompletoCreate


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

    @staticmethod
    def get_by_chat_id(db: Session, chat_id: str):
        """Obtener pedidos por chat_id"""
        pedidos = db.exec(select(Pedido).where(Pedido.chat_id == chat_id)).all()
        return pedidos

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

    @staticmethod
    def crear_pedido_completo(db: Session, pedido_completo: PedidoCompletoCreate):
        """Crear un pedido completo con sus detalles"""
        print("pedido_completo:", pedido_completo)
        try:
            # Crear el pedido
            pedido_data = {
                "total": pedido_completo.total,
                "estado": pedido_completo.estado,
                "ubicacion_entrega": pedido_completo.ubicacion_entrega,
                "precio_delivery": pedido_completo.precio_delivery,
                "chat_id": pedido_completo.chat_id,
                "nombre_usuario": pedido_completo.nombre_usuario,
                "delivery_id": pedido_completo.delivery_id
            }
            db_pedido = Pedido(**pedido_data)
            db.add(db_pedido)
            db.flush()  # Para obtener el ID del pedido sin hacer commit
            
            # Verificar que el pedido tiene ID
            if db_pedido.id is None:
                raise ValueError("No se pudo generar el ID del pedido")
            
            # Crear los detalles asociados al pedido
            detalles_creados = []
            for detalle_data in pedido_completo.detalles:
                db_detalle = Detalle(
                    cantidad=detalle_data.cantidad,
                    observacion=detalle_data.observacion,
                    pedido_id=db_pedido.id,
                    plato_id=detalle_data.plato_id
                )
                db.add(db_detalle)
                detalles_creados.append(db_detalle)
            
            # Confirmar toda la transacción
            db.commit()
            db.refresh(db_pedido)
            
            # Refrescar los detalles
            for detalle in detalles_creados:
                db.refresh(detalle)
            
            return db_pedido
        
        except Exception as e:
            db.rollback()
            raise e
