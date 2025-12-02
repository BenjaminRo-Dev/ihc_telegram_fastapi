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
                                },
                            }
                        ]
                    ]
                },
            },
        )
        print("Url:", f"{MINIAPP}?chat_id={chat_id}&nombre_usuario={nombre_usuario}")


async def resumen_pedido(pedido):
    print("Pedido:", pedido)
    mensaje = "🧾 *Resumen de tu pedido:*\n\n"

    mensaje += f"*Cliente:* {pedido.nombre_usuario}\n"
    # mensaje += f"*Estado:* {pedido.estado}\n"
    # mensaje += f"*Ubicación de entrega:* {pedido.ubicacion_entrega}\n"
    mensaje += f"*Precio de delivery:* Bs{pedido.precio_delivery:.2f}\n\n"

    mensaje += "*Detalles:*\n"
    for detalle in pedido.detalles:
        mensaje += f"- {detalle.plato.nombre} x{detalle.cantidad}"
        if detalle.observacion:
            mensaje += f" (Obs: {detalle.observacion})"
        mensaje += "\n"

    mensaje += f"\n*Total a pagar:* Bs{pedido.total:.2f}"

    async with httpx.AsyncClient() as client:
        await client.post(
            f"{BOT}/sendMessage",
            json={
                "chat_id": int(pedido.chat_id),
                "text": mensaje,
                "parse_mode": "Markdown",
            },
        )


async def estado_pedido(pedido):
    mensaje = f"🚚 Tu pedido está: *{pedido.estado}*"
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{BOT}/sendMessage",
            json={
                "chat_id": int(pedido.chat_id),
                "text": mensaje,
                "parse_mode": "Markdown",
            },
        )
