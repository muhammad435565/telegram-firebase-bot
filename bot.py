from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters, ConversationHandler
import firebase_admin
from firebase_admin import credentials, firestore
import os, json

# Firebase setup
cred = credentials.Certificate(json.loads(os.getenv('FIREBASE_CRED')))
firebase_admin.initialize_app(cred)
db = firestore.client()

# Bot states
EMAIL, NUMBER = range(2)
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Apna email bheje.")
    return EMAIL

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['email'] = update.message.text
    await update.message.reply_text("Shukriya! Ab apna number bheje.")
    return NUMBER

async def get_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['number'] = update.message.text
    db.collection('users').add(user_data)
    await update.message.reply_text("Data save ho gaya. Shukriya!")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancel kar diya gaya.")
    return ConversationHandler.END

# App run
app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
        NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_number)],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)

app.add_handler(conv_handler)
app.run_polling()
