from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from supabase import create_client
import os

ADMIN_ID = 956357652

SUPABASE_URL = os.getenv(“SUPABASE_URL”)
SUPABASE_KEY = os.getenv(“SUPABASE_KEY”)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text(“Bot işləyir.”)

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
if update.effective_user.id != ADMIN_ID:
return

text = " ".join(context.args).upper()
if not text:
    await update.message.reply_text("Nömrə yaz.")
    return
supabase.table("nomreler").insert({
    "nomre": text
}).execute()
await update.message.reply_text("Əlavə edildi.")

async def check_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
text = update.message.text.strip().upper()

result = (
    supabase.table("nomreler")
    .select("nomre")
    .eq("nomre", text)
    .execute()
)
if result.data:
    await update.message.reply_text("Nömrə sistemdə mövcuddur")
else:
    await update.message.reply_text("Qeydiyyatı yoxdur")

app = Application.builder().token(“8949021536:AAFXX8r7I0J166Z5fraqpugc-76vFSPyMWM”).build()

app.add_handler(CommandHandler(“start”, start))
app.add_handler(CommandHandler(“add”, add))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_number))

app.run_polling()
