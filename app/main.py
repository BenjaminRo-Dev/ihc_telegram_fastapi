from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.cors import configuracion_cors
from app.core.database import init_db
from app.routers import (
    bot_router,
    delivery_router,
    categoria_router,
    plato_router,
    pedido_router,
    detalle_router,
    configuracion_router
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando aplicación...")
    init_db()
    yield
    print("Cerrando aplicación...")

app = FastAPI(
    title="Sistema de Pedidos con Telegram y FastAPI",
    lifespan=lifespan
)

configuracion_cors(app)

@app.get("/")
def root():
    return {"message": "Backend Telegram funcionando =)"}


app.include_router(bot_router.router)
app.include_router(delivery_router.router)
app.include_router(categoria_router.router)
app.include_router(plato_router.router)
app.include_router(pedido_router.router)
app.include_router(detalle_router.router)
app.include_router(configuracion_router.router)


