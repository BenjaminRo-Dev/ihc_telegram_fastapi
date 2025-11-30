from fastapi import APIRouter, Request
from app.services.telegram_service import abrir_menu, enviar_mensaje

router = APIRouter(tags=["Telegram Bot"])

@router.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        texto = data["message"].get("text", "").lower()
        print("Texto recibido:", texto)

        if texto == "/iniciar":
            print("chat_id:", chat_id)
            await enviar_mensaje(chat_id, "👋 ¡Bienvenido al sistema de pedidos!")
        elif texto == "/menu":
            await abrir_menu(chat_id)
        else:
            await enviar_mensaje(chat_id, f"Recibí tu mensaje: {texto}")

    return {"ok": True}
