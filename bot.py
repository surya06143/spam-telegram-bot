import pickle
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

# ==========================
# Load the trained AI model
# ==========================

with open("spam_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# ==========================
# Telegram Bot Token
# ==========================

BOT_TOKEN = "8773669212:AAE5br5ItgfTy9gvpErEu04Dq-udOKYb0jQ"

# ==========================
# Handle incoming messages
# ==========================

async def detect_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text

    message_vector = vectorizer.transform([user_message])

    prediction = model.predict(message_vector)

    if prediction[0] == 1:
        reply = "🚨 This message is SPAM."
    else:
        reply = "✅ This message is HAM (Not Spam)."

    await update.message.reply_text(reply)

# ==========================
# Start the Bot
# ==========================

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, detect_spam))

print("Bot is running...")

app.run_polling()