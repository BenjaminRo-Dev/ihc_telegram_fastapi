from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.responses import HTMLResponse
from app.core.cors import configuracion_cors
from app.core.database import init_db
from app.routers import (
    bot_router,
    usuario_router,
    delivery_router,
    categoria_router,
    plato_router,
    pedido_router,
    detalle_router
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

# @app.get("/")
# def root():
#     return {"message": "Backend Telegram funcionando =)"}

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <head>
            <meta charset="UTF-8" />
            <script src="https://telegram.org/js/telegram-web-app.js"></script>
        </head>
        <body>
            <h1 style="text-align:center;">Hola Mundo =)</h1>

            <script>
                const tg = window.Telegram.WebApp;
                tg.expand();
            </script>
        </body>
    </html>
    """


app.include_router(bot_router.router)
app.include_router(usuario_router.router)
app.include_router(delivery_router.router)
app.include_router(categoria_router.router)
app.include_router(plato_router.router)
app.include_router(pedido_router.router)
app.include_router(detalle_router.router)


