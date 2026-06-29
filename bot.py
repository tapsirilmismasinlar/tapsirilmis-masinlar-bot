from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from supabase import create_client

ADMIN_ID = 956357652

SUPABASE_URL = "https://qbvzqcitdewggwmjjpcf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFidnpxY2l0ZGV3Z2d3bWpqcGNmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODEzNTA3NDMsImV4cCI6MjA5NjkyNjc0M30.XOkQvTrDCoiNpua8GTaEbXpIGYvq_hIm6-9SqqWcgNU"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


async def save_user(user_id):
    try:
        result = supabase.table("users").select("user_id").eq("user_id", user_id).execute()

        if not result.data:
            supabase.table("users").insert({"user_id": user_id}).execute()
    except:
        pass


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await save_user(update.effective_user.id)
    await update.message.reply_text("Bot isleyir.")


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await save_user(update.effective_user.id)

    if update.effective_user.id != ADMIN_ID:
        return

    text = " ".join(context.args).upper()

    if not text:
        await update.message.reply_text("Nomre yaz.")
        return

    try:
        supabase.table("nomreler").insert({"nomre": text}).execute()
        await update.message.reply_text("Elave edildi.")
    except Exception as e:
        await update.message.reply_text(f"Xeta: {e}")


async def list_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await save_user(update.effective_user.id)

    if update.effective_user.id != ADMIN_ID:
        return

    try:
        result = supabase.table("nomreler").select("nomre").execute()

        if not result.data:
            await update.message.reply_text("Nomre yoxdur.")
            return

        nomreler = [row["nomre"] for row in result.data]

        for i in range(0, len(nomreler), 100):
            await update.message.reply_text("\n".join(nomreler[i:i+100]))

    except Exception as e:
        await update.message.reply_text(f"Xeta: {e}")


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await save_user(update.effective_user.id)

    if update.effective_user.id != ADMIN_ID:
        return

    result = supabase.table("users").select("user_id").execute()

    await update.message.reply_text(
        f"Istifadeci sayi: {len(result.data)}"
    )


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await save_user(update.effective_user.id)

    if update.effective_user.id != ADMIN_ID:
        return

    text = " ".join(context.args)

    if not text:
        await update.message.reply_text("Mesaj yaz.")
        return

    users = supabase.table("users").select("user_id").execute()

    sent = 0

    for user in users.data:
        try:
            await context.bot.send_message(user["user_id"], text)
            sent += 1
        except:
            pass

    await update.message.reply_text(f"{sent} neferə gonderildi.")
async def delete_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await save_user(update.effective_user.id)

    if update.effective_user.id != ADMIN_ID:
        return

    text = " ".join(context.args).upper()

    if not text:
        await update.message.reply_text("Nomre yaz.")
        return

    try:
        supabase.table("nomreler").delete().eq("nomre", text).execute()
        await update.message.reply_text("Silindi.")
    except Exception as e:
        await update.message.reply_text(f"Xeta: {e}")


async def count_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await save_user(update.effective_user.id)

    if update.effective_user.id != ADMIN_ID:
        return

    result = supabase.table("nomreler").select("nomre").execute()

    await update.message.reply_text(
        f"Umumi nomre sayi: {len(result.data)}"
    )

async def check_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await save_user(update.effective_user.id)

    text = update.message.text.strip().upper()

    try:
        result = (
            supabase.table("nomreler")
            .select("nomre")
            .eq("nomre", text)
            .execute()
        )

        if result.data:
            await update.message.reply_text("Movcuddur")
        else:
            await update.message.reply_text("Yoxdur")

    except Exception as e:
        await update.message.reply_text(f"Xeta: {e}")


app = Application.builder().token("8949021536:AAHpfn8Sss6V7n8KFAAIKiaBQC7NzN5mwEc").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("list", list_numbers))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(CommandHandler("del", delete_number))
app.add_handler(CommandHandler("count", count_numbers))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_number))

app.run_polling()
