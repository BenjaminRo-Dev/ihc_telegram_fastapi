import httpx
from app.core.config import settings

BOT = settings.TELEGRAM_BOT
MINIAPP = settings.FRONTEND

async def enviar_mensaje(chat_id: int, text: str):
    async with httpx.AsyncClient() as client:
        await client.post(f"{BOT}/sendMessage", json={"chat_id": chat_id, "text": text})


async def abrir_app(chat_id: int, nombre_usuario: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{BOT}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": "🍽️ Realiza tu pedido aqui:",
                "reply_markup": {
                    "inline_keyboard": [
                        [
                            {
                                "text": "ComeYa App",
                                "web_app": {
                                    "url": f"{MINIAPP}?chat_id={chat_id}&nombre_usuario={nombre_usuario}"
                                }
                            }
                        ]
                    ]
                }
            }
        )