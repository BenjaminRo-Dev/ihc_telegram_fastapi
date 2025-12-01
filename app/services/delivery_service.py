from sqlmodel import Session, select
from app.models.modelos import Delivery, Configuracion
from app.schemas.delivery_schema import DeliveryCreate, DeliveryUpdate
from math import radians, sin, cos, sqrt, atan2


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
        deliveries = db.exec(select(Delivery).where(Delivery.disponible == True)).all()
        return deliveries

    @staticmethod
    def calcular_distancia_haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calcular la distancia en kilómetros entre dos puntos geográficos
        usando la fórmula de Haversine
        """
        # Radio de la Tierra en kilómetros
        R = 6371.0
        
        # Convertir grados a radianes
        lat1_rad = radians(lat1)
        lon1_rad = radians(lon1)
        lat2_rad = radians(lat2)
        lon2_rad = radians(lon2)
        
        # Diferencias
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        # Fórmula de Haversine
        a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        distancia = R * c
        return distancia

    @staticmethod
    def get_delivery_mas_cercano(db: Session):
        """
        Obtener el delivery disponible más cercano a la ubicación del restaurante.
        La ubicación se obtiene de la primera configuración en la tabla Configuracion.
        """
        # Obtener la configuración del restaurante
        configuracion = db.exec(select(Configuracion)).first()
        if not configuracion:
            raise ValueError("No se encontró configuración del restaurante")
        
        # Obtener todos los deliveries disponibles
        deliveries_disponibles = db.exec(select(Delivery).where(Delivery.disponible == True)).all()
        
        if not deliveries_disponibles:
            return None
        
        # Parsear la ubicación del restaurante
        try:
            lat_entrega, lon_entrega = map(float, configuracion.ubicacion_restaurante.split(','))
        except ValueError:
            raise ValueError("Formato de ubicación del restaurante inválido")
        
        delivery_mas_cercano = None
        distancia_minima = float('inf')
        
        # Calcular distancia para cada delivery disponible
        for delivery in deliveries_disponibles:
            try:
                lat_delivery, lon_delivery = map(float, delivery.ubicacion.split(','))
                distancia = DeliveryService.calcular_distancia_haversine(
                    lat_entrega, lon_entrega, lat_delivery, lon_delivery
                )
                
                if distancia < distancia_minima:
                    distancia_minima = distancia
                    delivery_mas_cercano = delivery
            except ValueError:
                # Si la ubicación del delivery no es válida, lo saltamos
                continue
        
        return delivery_mas_cercano

    @staticmethod
    def calcular_tarifa_delivery(db: Session, ubicacion_entrega: str) -> float:
        """
        Calcular la tarifa del delivery basándose en la distancia entre
        la ubicación de entrega y el restaurante.
        ubicacion_entrega debe estar en formato: "latitud,longitud"
        
        Fórmula: (distancia_km * precio_km) + precio_base
        """
        # Obtener la configuración del restaurante
        configuracion = db.exec(select(Configuracion)).first()
        if not configuracion:
            raise ValueError("No se encontró configuración del restaurante")
        
        # Parsear la ubicación del restaurante
        try:
            lat_restaurante, lon_restaurante = map(float, configuracion.ubicacion_restaurante.split(','))
        except ValueError:
            raise ValueError("Formato de ubicación del restaurante inválido")
        
        # Parsear la ubicación de entrega
        try:
            lat_entrega, lon_entrega = map(float, ubicacion_entrega.split(','))
        except ValueError:
            raise ValueError("Formato de ubicación de entrega inválido. Use: 'latitud,longitud'")
        
        # Calcular distancia en kilómetros
        distancia_km = DeliveryService.calcular_distancia_haversine(
            lat_restaurante, lon_restaurante, lat_entrega, lon_entrega
        )
        
        # Calcular tarifa: (distancia * precio_km) + precio_base
        tarifa = (distancia_km * configuracion.precio_km) + configuracion.precio_base
        
        return tarifa
