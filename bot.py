import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
QUOTEX_LINK = "https://broker-qx.pro/sign-up/?lid=1676502"
VIP_GROUP_LINK = "https://t.me/+jiePNdiDIfU5ZGM1"
YOUTUBE_LINK = "https://youtube.com/@TSBOWNERPRINCE"

pending_users = {}

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("🌐 Open New Account", url=QUOTEX_LINK)],
        [InlineKeyboardButton("📹 How to Open & Verify", url=YOUTUBE_LINK)],
        [InlineKeyboardButton("✅ Submit Quotex ID", callback_data="submit_id")]
    ]
    await update.message.reply_text(
        f"🔴 *Trading School BD - VERIFY Bot*\n\n"
        f"সগতম {user.first_name}! 👋\n\n"
        f"VIP Group এ join করতে:\n\n"
        f"*Step 1:* নিচের লিংক থেকে Quotex এ account খুলুন\n"
        f"*Step 2:* KYC verification করুন\n"
        f"*Step 3:* Quotex ID submit করুন\n\n"
        f"✅ Verify হলে VIP Group link পাবেন!",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "submit_id":
        await query.message.reply_text(
            "📝 আপনার *Quotex ID* send করুন:\nExample: `123456789`",
            parse_mode="Markdown"
        )
        context.user_data["waiting_for_id"] = True
    elif query.data.startswith("approve_"):
        user_id = int(query.data.split("_")[1])
        quotex_id = pending_users.get(user_id, {}).get("quotex_id", "Unknown")
        keyboard = [[InlineKeyboardButton("🎯 Join VIP Group", url=VIP_GROUP_LINK)]]
        await context.bot.send_message(
            chat_id=user_id,
            text=f"✅ *Congratulations!*\n\nQuotex ID *{quotex_id}* verify হয়েছে!\nVIP Group এ join করুন 👇",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        await query.message.edit_text(f"✅ Approved! Quotex ID: {quotex_id}")
    elif query.data.startswith("reject_"):
        user_id = int(query.data.split("_")[1])
        await context.bot.send_message(
            chat_id=user_id,
            text="❌ *Verification Failed*\n\nসঠিক ID দিয়ে আবার চেষ্টা করুন।",
            parse_mode="Markdown"
        )
        await query.message.edit_text("❌ Rejected.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    if context.user_data.get("waiting_for_id"):
        if text.isdigit() and len(text) >= 6:
            context.user_data["waiting_for_id"] = False
            pending_users[user.id] = {"quotex_id": text}
            admin_keyboard = [[
                InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")
            ]]
            try:
                await context.bot.send_message(
                    chat_id="@TSBOWNERPRINCE",
                    text=f"🔔 *New Verification*\n\n👤 {user.first_name}\n🆔 @{user.username}\n📊 Quotex ID: `{text}`",
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup(admin_keyboard)
                )
            except:
                pass
            await update.message.reply_text(
                "✅ *Submit হয়েছে!*\n\n১-২ ঘণ্টার মধ্যে verify হবে। 🕐",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text("❌ সঠিক Quotex ID দিন! শুধু numbers। Example: `123456789`", parse_mode="Markdown")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
