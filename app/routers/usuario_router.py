from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_session
from app.services.usuario_service import UsuarioService
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate, UsuarioResponse

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.get("/", response_model=list[UsuarioResponse])
def get_usuarios(db: Session = Depends(get_session)):
    """Obtener todos los usuarios"""
    return UsuarioService.get_all(db)


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def get_usuario(usuario_id: int, db: Session = Depends(get_session)):
    """Obtener un usuario por ID"""
    usuario = UsuarioService.get_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.post("/", response_model=UsuarioResponse, status_code=201)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_session)):
    """Crear un nuevo usuario"""
    return UsuarioService.create(db, usuario)


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def update_usuario(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_session)):
    """Actualizar un usuario existente"""
    db_usuario = UsuarioService.update(db, usuario_id, usuario)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario


@router.delete("/{usuario_id}", response_model=UsuarioResponse)
def delete_usuario(usuario_id: int, db: Session = Depends(get_session)):
    """Eliminar un usuario"""
    db_usuario = UsuarioService.delete(db, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario
