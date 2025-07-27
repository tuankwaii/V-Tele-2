from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import os

user_ids = {}

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("💰 Nạp tiền", callback_data='nap')],
        [InlineKeyboardButton("🛟 Hỗ trợ", callback_data='hotro')],
        [InlineKeyboardButton("🎮 ID Game", callback_data='idgame')]
    ]
    update.message.reply_text("Chào mừng bạn đến với bot!", reply_markup=InlineKeyboardMarkup(keyboard))

def gid(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        update.message.reply_text("❌ Sai cú pháp. Vui lòng dùng:\n/gid [ID Game]\nVí dụ: /gid 123456789")
        return
    user_id = update.message.from_user.id
    user_ids[user_id] = context.args[0]
    update.message.reply_text("✅ Cập nhật ID Game thành công!")

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    query.answer()

    if query.data == 'nap':
        ma_nap = f"DONE{str(user_id)[-6:].upper()}"
        message = f"""💳 *Cách nạp tiền qua NGÂN HÀNG (tối thiểu 100k)*:

➡️ Ngân hàng: *VIB*
➡️ Số tài khoản: *073840887* (ấn để copy)
➡️ Tên tài khoản: *Le Thi Ngoc Hoa*
➡️ Nội dung chuyển: *{ma_nap}*

*⏳ Lưu ý:* Mã nạp có hiệu lực trong 10 phút và chỉ nạp 1 lần.
Dùng lệnh /nap để lấy mã mới nếu cần.

🆘 Nếu sau 2-3 phút chưa nhận được, hãy liên hệ hỗ trợ.
"""
        query.edit_message_text(message, parse_mode='Markdown')

    elif query.data == 'hotro':
        keyboard = [
            [InlineKeyboardButton("💬 Chat với Admin", url="https://t.me/hotro3bett")]
        ]
        query.edit_message_text("🛟 Trung tâm hỗ trợ:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'idgame':
        if user_id in user_ids:
            query.edit_message_text(f"🎮 ID Game của bạn là: `{user_ids[user_id]}`", parse_mode='Markdown')
        else:
            query.edit_message_text("⚠️ Bạn chưa cài đặt ID Game\n\nHãy dùng cú pháp:\n/gid [ID Game]\nVí dụ: /gid 123456789")

def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("gid", gid))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
