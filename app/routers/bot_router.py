from fastapi import APIRouter, Request
from app.services.telegram_service import send_message

router = APIRouter(tags=["Telegram Bot"])

@router.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "").lower()

        if text == "/start":
            await send_message(chat_id, "👋 ¡Bienvenido al sistema de pedidos!")
        elif text == "/menu":
            await send_message(chat_id, "🍕 Menú:\n1. Pizza\n2. Hamburguesa\n3. Ensalada")
        else:
            await send_message(chat_id, f"Recibí tu mensaje: {text}")

    return {"ok": True}
