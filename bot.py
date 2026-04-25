import os
import anthropic
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text:
        return
    
    # Group এ শুধু /ask দিয়ে কথা বলা যাবে
    if update.message.chat.type != "private":
        if not text.startswith("/ask"):
            return
        text = text.replace("/ask", "").strip()
    
    await update.message.reply_text("⏳ ভাবছি...")
    
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": text}]
    )
    
    await update.message.reply_text(response.content[0].text)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle))
app.run_polling()
