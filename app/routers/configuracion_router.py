from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_session
from app.services.configuracion_service import ConfiguracionService
from app.schemas.configuracion_schema import ConfiguracionCreate, ConfiguracionUpdate, ConfiguracionResponse

router = APIRouter(
    prefix="/configuraciones",
    tags=["Configuraciones"]
)


@router.get("/", response_model=list[ConfiguracionResponse])
def get_configuraciones(db: Session = Depends(get_session)):
    """Obtener todas las configuraciones"""
    return ConfiguracionService.get_all(db)


@router.get("/{configuracion_id}", response_model=ConfiguracionResponse)
def get_configuracion(configuracion_id: int, db: Session = Depends(get_session)):
    """Obtener una configuración por ID"""
    configuracion = ConfiguracionService.get_by_id(db, configuracion_id)
    if not configuracion:
        raise HTTPException(status_code=404, detail="Configuración no encontrada")
    return configuracion


@router.post("/", response_model=ConfiguracionResponse, status_code=201)
def create_configuracion(configuracion: ConfiguracionCreate, db: Session = Depends(get_session)):
    """Crear una nueva configuración"""
    return ConfiguracionService.create(db, configuracion)


@router.put("/{configuracion_id}", response_model=ConfiguracionResponse)
def update_configuracion(configuracion_id: int, configuracion: ConfiguracionUpdate, db: Session = Depends(get_session)):
    """Actualizar una configuración existente"""
    db_configuracion = ConfiguracionService.update(db, configuracion_id, configuracion)
    if not db_configuracion:
        raise HTTPException(status_code=404, detail="Configuración no encontrada")
    return db_configuracion


@router.delete("/{configuracion_id}", response_model=ConfiguracionResponse)
def delete_configuracion(configuracion_id: int, db: Session = Depends(get_session)):
    """Eliminar una configuración"""
    db_configuracion = ConfiguracionService.delete(db, configuracion_id)
    if not db_configuracion:
        raise HTTPException(status_code=404, detail="Configuración no encontrada")
    return db_configuracion
