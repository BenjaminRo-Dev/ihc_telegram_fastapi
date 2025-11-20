from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

def configuracion_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
