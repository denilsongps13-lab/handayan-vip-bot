import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ.get("SUPPORT_BOT_TOKEN")
ADMIN_TELEGRAM_ID = os.environ.get("ADMIN_TELEGRAM_ID")

PORT = int(os.environ.get("PORT", "10000"))
WEBHOOK_URL = os.environ.get("RENDER_EXTERNAL_URL")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "💳 Problema com pagamento",
                callback_data="pagamento",
            )
        ],
        [
            InlineKeyboardButton(
                "🔐 Problema com acesso VIP",
                callback_data="acesso",
            )
        ],
        [
            InlineKeyboardButton(
                "💬 Outras dúvidas",
                callback_data="outros",
            )
        ],
    ]

    await update.message.reply_text(
        "💬 Soporte Handayan VIP\n\n"
        "Hola ❤️ ¿Cómo podemos ayudarte?\n\n"
        "Selecciona una opción 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def botoes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "pagamento":
        context.user_data["assunto"] = "💳 PAGAMENTO"

        texto = (
            "💳 Soporte de pago\n\n"
            "Cuéntame qué problema tuviste con el pago.\n\n"
            "Escribe tu mensaje aquí 👇"
        )

    elif query.data == "acesso":
        context.user_data["assunto"] = "🔐 ACESSO VIP"

        texto = (
            "🔐 Soporte de acceso VIP\n\n"
            "Cuéntame qué problema tuviste para entrar al VIP.\n\n"
            "Escribe tu mensaje aquí 👇"
        )

    else:
        context.user_data["assunto"] = "💬 OUTRA DÚVIDA"

        texto = (
            "💬 Soporte general\n\n"
            "Escribe tu duda o mensaje aquí 👇"
        )

    await query.edit_message_text(texto)


async def receber_mensagem(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message or not update.message.text:
        return

    assunto = context.user_data.get(
        "assunto",
        "💬 SUPORTE",
    )

    user = update.effective_user

    nome = user.full_name if user else "Usuário"

    if user and user.username:
        username = f"@{user.username}"
    else:
        username = "Sem username"

    user_id = user.id if user else "Desconhecido"

    texto_admin = (
        f"{assunto}\n\n"
        f"👤 Cliente: {nome}\n"
        f"🔗 Username: {username}\n"
        f"🆔 Telegram ID: {user_id}\n\n"
        f"📝 Mensagem:\n"
        f"{update.message.text}"
    )

    try:
        await context.bot.send_message(
            chat_id=int(ADMIN_TELEGRAM_ID),
            text=texto_admin,
        )

        await update.message.reply_text(
            "✅ Mensaje enviado al soporte.\n\n"
            "Te responderemos lo antes posible ❤️"
        )

    except Exception as erro:
        print(f"Erro ao encaminhar mensagem: {erro}")

        await update.message.reply_text(
            "⚠️ No fue posible enviar tu mensaje ahora.\n\n"
            "Inténtalo nuevamente en unos minutos."
        )


def main():
    if not TOKEN:
        raise RuntimeError(
            "SUPPORT_BOT_TOKEN não configurado"
        )

    if not ADMIN_TELEGRAM_ID:
        raise RuntimeError(
            "ADMIN_TELEGRAM_ID não configurado"
        )

    if not WEBHOOK_URL:
        raise RuntimeError(
            "RENDER_EXTERNAL_URL não disponível"
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            botoes,
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            receber_mensagem,
        )
    )

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="support",
        webhook_url=f"{WEBHOOK_URL}/support",
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
