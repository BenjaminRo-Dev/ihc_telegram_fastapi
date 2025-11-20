import httpx
from app.core.config import settings

BASE_URL = f"https://api.telegram.org/bot{settings.BOT_TOKEN}"

async def send_message(chat_id: int, text: str):
    async with httpx.AsyncClient() as client:
        await client.post(f"{BASE_URL}/sendMessage", json={"chat_id": chat_id, "text": text})
