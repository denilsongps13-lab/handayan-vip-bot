import os
from datetime import datetime, timedelta, timezone

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    LabeledPrice,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    PreCheckoutQueryHandler,
    MessageHandler,
    filters,
)

TOKEN = os.environ.get("BOT_TOKEN")
PORT = int(os.environ.get("PORT", "10000"))
WEBHOOK_URL = "https://handayan-vip-bot.onrender.com"
VIP_CHANNEL_ID = int(os.environ.get("VIP_CHANNEL_ID", "0"))

VIP_PRICE_STARS = 100
VIP_PAYLOAD = "handayan_vip_100"
SUPPORT_URL = "https://t.me/HandayanVIPSuporteBot"


def menu_principal():
    return [
        [InlineKeyboardButton("💎 ENTRAR NO VIP", callback_data="vip")],
        [InlineKeyboardButton("🔥 Ver conteúdo", callback_data="conteudo")],
        [InlineKeyboardButton("💬 Falar comigo", callback_data="falar")],
    ]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💋 Hola, amor. Soy Handayan ❤️\n\n"
        "Bienvenido a mi espacio privado 🔥\n\n"
        "Aquí vas a descubrir contenido exclusivo "
        "y un lado mío que no encontrarás en mis redes.\n\n"
        "Elige una opción abajo 👇",
        reply_markup=InlineKeyboardMarkup(menu_principal()),
    )


async def botoes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "vip":
        keyboard = [
            [
                InlineKeyboardButton(
                    "⭐ Assinar por 100 Stars",
                    callback_data="assinar",
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Voltar",
                    callback_data="voltar",
                )
            ],
        ]

        await query.edit_message_text(
            "💎 HANDAYAN VIP 💎\n\n"
            "🔥 Contenido exclusivo\n"
            "📸 Fotos especiales\n"
            "🎬 Videos privados\n"
            "❤️ Novedades VIP\n"
            "🔐 Acceso al canal privado\n\n"
            "Precio: ⭐ 100 Stars\n\n"
            "Toca abajo para liberar tu acceso 👇",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "assinar":
        await context.bot.send_invoice(
            chat_id=query.message.chat_id,
            title="Handayan VIP",
            description="Acceso al canal privado Handayan VIP.",
            payload=VIP_PAYLOAD,
            currency="XTR",
            prices=[
                LabeledPrice(
                    "Handayan VIP",
                    VIP_PRICE_STARS,
                )
            ],
        )

    elif query.data == "conteudo":
        keyboard = [
            [
                InlineKeyboardButton(
                    "💎 QUERO SER VIP",
                    callback_data="vip",
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Voltar",
                    callback_data="voltar",
                )
            ],
        ]

        await query.edit_message_text(
            "🔥 CONTENIDO HANDAYAN 🔥\n\n"
            "En el VIP encontrarás:\n\n"
            "📸 Fotos exclusivas\n"
            "🎬 Videos privados\n"
            "💋 Contenido especial\n"
            "❤️ Novedades de Handayan\n\n"
            "¿Quieres entrar? 👇",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "falar":
        keyboard = [
            [
                InlineKeyboardButton(
                    "💬 ABRIR SUPORTE",
                    url=SUPPORT_URL,
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Voltar",
                    callback_data="voltar",
                )
            ],
        ]

        await query.edit_message_text(
            "💬 SOPORTE HANDAYAN VIP\n\n"
            "¿Necesitas ayuda con tu pago o acceso VIP? ❤️\n\n"
            "Toca el botón abajo para hablar con nuestro soporte 👇",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "voltar":
        await query.edit_message_text(
            "💋 Hola, amor. Soy Handayan ❤️\n\n"
            "Bienvenido a mi espacio privado 🔥\n\n"
            "Elige una opción abajo 👇",
            reply_markup=InlineKeyboardMarkup(menu_principal()),
        )


async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query

    if query.invoice_payload != VIP_PAYLOAD:
        await query.answer(
            ok=False,
            error_message="No fue posible validar este pedido.",
        )
        return

    await query.answer(ok=True)


async def pagamento_confirmado(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    pagamento = update.message.successful_payment

    pagamento_valido = (
        pagamento.currency == "XTR"
        and pagamento.invoice_payload == VIP_PAYLOAD
        and pagamento.total_amount == VIP_PRICE_STARS
    )

    if not pagamento_valido:
        return

    try:
        expira_em = datetime.now(timezone.utc) + timedelta(hours=24)

        convite = await context.bot.create_chat_invite_link(
            chat_id=VIP_CHANNEL_ID,
            expire_date=expira_em,
            member_limit=1,
            name=f"VIP-{update.effective_user.id}",
        )

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💎 ENTRAR NO CANAL VIP",
                        url=convite.invite_link,
                    )
                ]
            ]
        )

        await update.message.reply_text(
            "✅ PAGAMENTO CONFIRMADO! 💎\n\n"
            "Bienvenido a Handayan VIP ❤️🔥\n\n"
            "Tu enlace es personal y puede ser utilizado "
            "por una sola persona.\n\n"
            "⏳ El enlace expira en 24 horas.\n\n"
            "Toca abajo para entrar 👇",
            reply_markup=keyboard,
        )

    except Exception as erro:
        print(f"Erro ao criar convite VIP: {erro}")

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💬 FALAR COM SUPORTE",
                        url=SUPPORT_URL,
                    )
                ]
            ]
        )

        await update.message.reply_text(
            "✅ Tu pago fue confirmado.\n\n"
            "⚠️ No fue posible generar tu enlace VIP automáticamente.\n\n"
            "Habla con nuestro soporte 👇",
            reply_markup=keyboard,
        )


async def paysupport(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "💬 ABRIR SUPORTE",
                    url=SUPPORT_URL,
                )
            ]
        ]
    )

    await update.message.reply_text(
        "💳 SOPORTE DE PAGOS\n\n"
        "¿Tuviste algún problema con tu compra o acceso VIP?\n\n"
        "Toca abajo para hablar con nuestro soporte ❤️",
        reply_markup=keyboard,
    )


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN não configurado")

    if not VIP_CHANNEL_ID:
        raise RuntimeError("VIP_CHANNEL_ID não configurado")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("paysupport", paysupport))
    app.add_handler(CallbackQueryHandler(botoes))
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(
        MessageHandler(
            filters.SUCCESSFUL_PAYMENT,
            pagamento_confirmado,
        )
    )

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="telegram",
        webhook_url=f"{WEBHOOK_URL}/telegram",
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
