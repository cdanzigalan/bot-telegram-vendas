import socket

# força uso de IPv4 (resolve timeout com Telegram)
def force_ipv4():
    orig_getaddrinfo = socket.getaddrinfo

    def getaddrinfo_ipv4(*args, **kwargs):
        return [res for res in orig_getaddrinfo(*args, **kwargs) if res[0] == socket.AF_INET]

    socket.getaddrinfo = getaddrinfo_ipv4

force_ipv4()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "7984594290:AAGZYMSoSPsrvsWF5a_2uUMUlrn5u2nByh4"
PIX = "https://livepix.gg/melissacostelli"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = """
Oi, amor 😘

Seja bem-vindo ao meu conteúdo exclusivo 🔥

Aqui você encontra conteúdos privados que não posto em nenhum outro lugar.

💎 Acesso completo
🔥 Conteúdo exclusivo
🔒 Entrada liberada após confirmação do Pix

Valor: R$ 14,90

Clique abaixo para comprar 👇
"""

    teclado = InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 COMPRAR ACESSO", callback_data="comprar")]
    ])

    await update.message.reply_text(texto, reply_markup=teclado)


async def comprar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    texto_pix = f"""
Perfeito 😈

Para liberar seu acesso, faça o pagamento:

💰 Valor: R$ 14,90

🔑 Pagar aqui:
{PIX}

Após o pagamento, envie o comprovante aqui no chat 📩

Assim que eu confirmar, libero seu acesso ao canal privado 🔓
"""

    await query.message.reply_text(texto_pix)


def main():
    print("Iniciando bot...")

    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .connect_timeout(60)
        .read_timeout(60)
        .write_timeout(60)
        .pool_timeout(60)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(comprar, pattern="comprar"))

    print("Bot rodando. Abra o Telegram e mande /start para ele.")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()