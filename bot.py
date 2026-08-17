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
        pagamento.currency == "
