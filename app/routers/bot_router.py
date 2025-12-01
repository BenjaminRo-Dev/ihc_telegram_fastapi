from fastapi import APIRouter, Request
from app.services.telegram_service import abrir_app, enviar_mensaje

router = APIRouter(tags=["Telegram Bot"])


@router.post("/webhook")
async def telegram_webhook(request: Request):

    data = await request.json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        nombre_usuario = data["message"]["from"]["first_name"]
        texto = data["message"].get("text", "").lower()

        if texto == "/iniciar":
            print({"chat_id": chat_id, "nombre_usuario": nombre_usuario})
            await abrir_app(chat_id, nombre_usuario)

    return {"ok": True}
