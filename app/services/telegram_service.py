import httpx
from app.core.config import settings

BOT = settings.TELEGRAM_BOT
MINIAPP = settings.FRONTEND

async def enviar_mensaje(chat_id: int, text: str):
    async with httpx.AsyncClient() as client:
        print("enviando mensaje")
        await client.post(f"{BOT}/sendMessage", json={"chat_id": chat_id, "text": text})
        print("mensaje enviado")


async def abrir_menu(chat_id: int):
    async with httpx.AsyncClient() as client:
        # print("abriendo menu")
        print(f"{MINIAPP}/menu")
        await client.post(
            f"{BOT}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": "🍽️ Aquí está el menú:",
                "reply_markup": {
                    "inline_keyboard": [
                        [
                            {
                                "text": "Abrir menú",
                                "web_app": {
                                    "url": f"{MINIAPP}/menu" #TODO: Esperar a que Tifanny acomode el front
                                }
                            }
                        ]
                    ]
                }
            }
        )
        print("menu abierto")