from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

ADMIN_ID = 123456789

numbers = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot işləyir.")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    text = " ".join(context.args)

    if not text:
        await update.message.reply_text("Nömrə yaz.")
        return

    numbers.append(text)
    await update.message.reply_text("Əlavə edildi.")

async def list_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not numbers:
        await update.message.reply_text("Nömrə yoxdur.")
        return

    await update.message.reply_text("\n".join(numbers))

app = Application.builder().token("BURAYA_TOKEN").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("list", list_numbers))

app.run_polling()
