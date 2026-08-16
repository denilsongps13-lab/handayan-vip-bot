import os

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

VIP_PRICE_STARS = 100
VIP_PAYLOAD = "handayan_vip_100"


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
            [InlineKeyboardButton("⭐ Assinar por 100 Stars", callback_data="assinar")],
            [InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")],
        ]

        await query.edit_message_text(
            "💎 HANDAYAN VIP 💎\n\n"
            "🔥 Conteúdo exclusivo\n"
            "❤️ Novidades especiais\n"
            "🔐 Acesso reservado para membros\n\n"
            "Preço: ⭐ 100 Stars\n\n"
            "Toque abaixo para assinar 👇",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "assinar":
        await context.bot.send_invoice(
            chat_id=query.message.chat_id,
            title="Handayan VIP",
            description="Acesso ao conteúdo VIP da Handayan.",
            payload=VIP_PAYLOAD,
            currency="XTR",
            prices=[LabeledPrice("Handayan VIP", VIP_PRICE_STARS)],
        )

    elif query.data == "conteudo":
        await query.edit_message_text(
            "🔥 Conteúdo da Handayan\n\n"
            "O conteúdo VIP será liberado automaticamente após o pagamento. ❤️",
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


async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query

    if query.invoice_payload != VIP_PAYLOAD:
        await query.answer(
            ok=False,
            error_message="Não foi possível validar este pedido."
        )
        return

    await query.answer(ok=True)


async def pagamento_confirmado(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    pagamento = update.message.successful_payment

    if (
        pagamento.currency == "XTR"
        and pagamento.invoice_payload == VIP_PAYLOAD
        and pagamento.total_amount == VIP_PRICE_STARS
    ):
        await update.message.reply_text(
            "✅ PAGAMENTO CONFIRMADO! 💎\n\n"
            "Bem-vindo ao Handayan VIP ❤️🔥\n\n"
            "Seu acesso VIP foi liberado.\n\n"
            "Em breve, todo o conteúdo exclusivo aparecerá por aqui."
        )


async def paysupport(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "💳 Suporte de pagamentos Handayan VIP\n\n"
        "Se você teve algum problema com uma compra, envie aqui uma mensagem "
        "explicando o que aconteceu e informe a data aproximada do pagamento."
    )


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN não configurado")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("paysupport", paysupport))
    app.add_handler(CallbackQueryHandler(botoes))
    app.add_handler(PreCheckoutQueryHandler(precheckout))

    app.add_handler(
        MessageHandler(
            filters.SUCCESSFUL_PAYMENT,
            pagamento_confirmado
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
