from sqlmodel import Session
from app.models.modelos import Delivery


def seed_delivery(session: Session):
    """Crea 5 deliveries de ejemplo"""
    deliveries_data = [
        {
            "nombre": "Benjamin Romero",
            "email": "benjamin@ihc.com",
            "password": "00000000",
            "ubicacion": "-17.78179532334912, -63.17222261216227", # Arenales
            "disponible": True
        },
        {
            "nombre": "Wilder Choque",
            "email": "wilder@ihc.com",
            "password": "00000000",
            "ubicacion": "-17.775093316805012, -63.19581532318543", #UAGRM
            "disponible": True
        },
        {
            "nombre": "Tifanny Pariona",
            "email": "tifanny@ihc.com",
            "password": "00000000",
            "ubicacion": "-17.794013578375374, -63.20399069609337", # av. piraí
            "disponible": False
        },
    ]

    for delivery_data in deliveries_data:
        ihc = Delivery(**delivery_data)
        session.add(ihc)
    
    session.commit()
    print("✓ Deliveries creados")
