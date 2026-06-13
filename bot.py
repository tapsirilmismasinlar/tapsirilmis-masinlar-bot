from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from supabase import create_client

ADMIN_ID = 956357652

SUPABASE_URL = "https://qbvzqcitdewggwmjjpcf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFidnpxY2l0ZGV3Z2d3bWpqcGNmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODEzNTA3NDMsImV4cCI6MjA5NjkyNjc0M30.XOkQvTrDCoiNpua8GTaEbXpIGYvq_hIm6-9SqqWcgNU"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot isleyir.")


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    text = " ".join(context.args).upper()

    if not text:
        await update.message.reply_text("Nomre yaz.")
        return

    supabase.table("nomreler").insert({"nomre": text}).execute()

    await update.message.reply_text("Elave edildi.")


async def check_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().upper()

    result = supabase.table("nomreler").select("nomre").eq("nomre", text).execute()

    if result.data:
        await update.message.reply_text("Movcuddur")
    else:
        await update.message.reply_text("Yoxdur")


app = Application.builder().token("8949021536:AAFXX8r7I0J166Z5fraqpugc-76vFSPyMWM").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_number))

app.run_polling()

