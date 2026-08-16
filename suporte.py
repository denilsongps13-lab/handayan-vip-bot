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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💳 Problema com pagamento", callback_data="pagamento")],
        [InlineKeyboardButton("🔐 Problema com acesso VIP", callback_data="acesso")],
        [InlineKeyboardButton("💬 Outras dúvidas", callback_data="outros")],
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
    if not update.message:
        return

    assunto = context.user_data.get("assunto", "💬 SUPORTE")

    user = update.effective_user

    nome = user.full_name if user else "Usuário"
    username = f"@{user.username}" if user and user.username else "Sem username"
    user_id = user.id if user else "Desconhecido"

    texto = (
        f"{assunto}\n\n"
        f"👤 Cliente: {nome}\n"
        f"🔗 Username: {username}\n"
        f"🆔 ID: {user_id}\n\n"
        f"📝 Mensagem:\n{update.message.text}"
    )

    admin_id = os.environ.get("ADMIN_TELEGRAM_ID")

    if not admin_id:
        await update.message.reply_text(
            "⚠️ El soporte todavía está siendo configurado."
        )
        return

    await context.bot.send_message(
        chat_id=int(admin_id),
        text=texto,
    )

    await update.message.reply_text(
        "✅ Mensaje enviado al soporte.\n\n"
        "Te responderemos lo antes posible ❤️"
    )


def main():
    if not TOKEN:
        raise RuntimeError("SUPPORT_BOT_TOKEN não configurado")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(botoes))
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            receber_mensagem,
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()
