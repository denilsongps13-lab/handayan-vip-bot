import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.environ.get("BOT_TOKEN")
PORT = int(os.environ.get("PORT", "10000"))
WEBHOOK_URL = "https://handayan-vip-bot.onrender.com"


def menu_principal():
    return [
        [InlineKeyboardButton("💎 ENTRAR NO VIP", callback_data="vip")],
        [InlineKeyboardButton("🔥 Ver conteúdo", callback_data="conteudo")],
        [InlineKeyboardButton("💬 Falar comigo", callback_data="falar")],
    ]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💋 Olá, amor! Eu sou a Handayan ❤️\n\n"
        "Bem-vindo ao meu espaço VIP 🔥\n\n"
        "Escolha uma opção abaixo 👇",
        reply_markup=InlineKeyboardMarkup(menu_principal()),
    )


async def botoes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "vip":
        keyboard = [
            [InlineKeyboardButton("💳 Assinar VIP", callback_data="assinar")],
            [InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")],
        ]

        await query.edit_message_text(
            "💎 HANDAYAN VIP 💎\n\n"
            "🔥 Conteúdo exclusivo\n"
            "❤️ Novidades especiais\n"
            "🔐 Acesso reservado para membros\n\n"
            "Escolha uma opção abaixo 👇",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "assinar":
        await query.edit_message_text(
            "💳 ASSINATURA VIP 💎\n\n"
            "Aqui vamos colocar o plano e o pagamento.\n\n"
            "Em breve você poderá assinar diretamente pelo bot. ❤️",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Voltar", callback_data="vip")]
            ]),
        )

    elif query.data == "conteudo":
        await query.edit_message_text(
            "🔥 Conteúdo da Handayan\n\n"
            "Novidades chegando em breve ❤️",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")]
            ]),
        )

    elif query.data == "falar":
        await query.edit_message_text(
            "💬 Quer falar comigo?\n\n"
            "Envie sua mensagem aqui ❤️",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")]
            ]),
        )

    elif query.data == "voltar":
        await query.edit_message_text(
            "💋 Olá, amor! Eu sou a Handayan ❤️\n\n"
            "Bem-vindo ao meu espaço VIP 🔥\n\n"
            "Escolha uma opção abaixo 👇",
            reply_markup=InlineKeyboardMarkup(menu_principal()),
        )


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN não configurado")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(botoes))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="telegram",
        webhook_url=f"{WEBHOOK_URL}/telegram",
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
