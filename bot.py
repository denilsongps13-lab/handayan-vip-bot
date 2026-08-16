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


# =========================
# CONFIGURAÇÕES
# =========================

TOKEN = os.environ.get("BOT_TOKEN")

PORT = int(os.environ.get("PORT", "10000"))

WEBHOOK_URL = "https://handayan-vip-bot.onrender.com"

VIP_CHANNEL_ID = int(
    os.environ.get("VIP_CHANNEL_ID", "0")
)

VIP_PRICE_STARS = 100

VIP_PAYLOAD = "handayan_vip_100"

SUPPORT_URL = "https://t.me/HandayanVIPSuporteBot"


# =========================
# MENU PRINCIPAL
# =========================

def menu_principal():
    return [
        [
            InlineKeyboardButton(
                "💎 ENTRAR NO VIP",
                callback_data="vip",
            )
        ],
        [
            InlineKeyboardButton(
                "🔥 Ver conteúdo",
                callback_data="conteudo",
            )
        ],
        [
            InlineKeyboardButton(
                "💬 Falar comigo",
                callback_data="falar",
            )
        ],
    ]


# =========================
# /START
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.message.reply_text(
        "💋 Hola, amor. Soy Handayan ❤️\n\n"
        "Bienvenido a mi espacio privado 🔥\n\n"
        "Aquí vas a descubrir contenido exclusivo "
        "y un lado mío que no encontrarás en mis redes.\n\n"
        "Elige una opción abajo 👇",
        reply_markup=InlineKeyboardMarkup(
            menu_principal()
        ),
    )


# =========================
# BOTÕES
# =========================

async def botoes(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query

    await query.answer()

    # VIP
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
            reply_markup=InlineKeyboardMarkup(
                keyboard
            ),
        )

    #
