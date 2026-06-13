from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

ADMIN_ID = 956357652

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

async def list_numbers(wait update.message.reply_text("\n".join(numbers))

async def check_number(update: Update, context):
    text = update.message.text.strip().upper()

    if text in numbers:
        await update.message.reply_text("Tapşırılıb")
    else:
        await update.message.reply_text("Tapşırılmayıb")):
    if not numbers:
        await update.message.reply_text("Nömrə yoxdur.")
        return

    await update.message.reply_text("\n".join(numbers))

app = Application.builder().token("8949021536:AAFXX8r7I0J166Z5fraqpugc-76vFSPyMWM").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("list", list_numbers))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_number))
app.run_polling()
