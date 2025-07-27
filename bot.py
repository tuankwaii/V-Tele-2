from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import os
from datetime import datetime, timedelta
import random

user_data = {}

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🔢 Nhập ID Game", callback_data='enter_id')],
        [InlineKeyboardButton("💰 Nạp tiền", callback_data='deposit')],
        [InlineKeyboardButton("🆘 Hỗ trợ", callback_data='support')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Chào mừng bạn đến với hệ thống!", reply_markup=reply_markup)

def generate_deposit_code():
    return "DONE" + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=6))

def handle_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    query.answer()
    data = query.data

    if data == "enter_id":
        context.bot.send_message(chat_id=user_id, text="Bạn chưa cài đặt ID Game\n\nĐể cập nhật ID Game cho tài khoản, sử dụng cú pháp:\n/gid [dấu cách] ID Game\n\nVD: /gid 123456789")
    elif data == "deposit":
        if user_id not in user_data or "game_id" not in user_data[user_id]:
            context.bot.send_message(chat_id=user_id, text="⚠️ Vui lòng nhập ID Game trước bằng lệnh /gid [ID]")
            return

        deposit_code = generate_deposit_code()
        user_data[user_id]["deposit_code"] = deposit_code
        user_data[user_id]["expire_time"] = datetime.now() + timedelta(minutes=10)

        msg = (
            "Chọn hình thức nạp tiền\n\n"
            "💳 Cách nạp tiền qua NGÂN HÀNG (tối thiểu 100k):\n"
            "➡️ Chuyển tiền vào ngân hàng: Vib\n"
            "➡️ Số tài khoản: 073840887 (ấn để copy)\n"
            "➡️ Tên tài khoản: Le Thi Ngoc Hoa\n\n"
            f"BẮT BUỘC nội dung chuyển là: {deposit_code} (ấn để copy)\n\n"
            "⏳ Mã nạp có hiệu lực 10 phút, chỉ dùng 1 lần.\n"
            "Gõ /nap để lấy lại thông tin nếu cần.\n\n"
            "🆘 Sau 2-3 phút nếu chưa vào hãy liên hệ CSKH."
        )
        context.bot.send_message(chat_id=user_id, text=msg)

    elif data == "support":
        context.bot.send_message(chat_id=user_id, text="🛠 Trung tâm hỗ trợ\n👉 Chat với admin: https://t.me/hotro3bett")

def gid(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if len(context.args) != 1:
        update.message.reply_text("Sai cú pháp! Dùng: /gid [ID Game]")
        return

    game_id = context.args[0]
    user_data[user_id] = {"game_id": game_id}
    update.message.reply_text("✅ Cập nhật ID Game thành công!")

def nap(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in user_data or "deposit_code" not in user_data[user_id]:
        update.message.reply_text("❗ Bạn chưa tạo mã nạp. Ấn vào nút Nạp tiền để tạo mã mới.")
        return

    expire_time = user_data[user_id].get("expire_time")
    if not expire_time or datetime.now() > expire_time:
        update.message.reply_text("❗ Mã nạp đã hết hạn. Ấn vào nút Nạp tiền để tạo mã mới.")
        return

    deposit_code = user_data[user_id]["deposit_code"]
    msg = (
        "💳 Cách nạp tiền qua NGÂN HÀNG (tối thiểu 100k):\n"
        "➡️ Chuyển tiền vào ngân hàng: Vib\n"
        "➡️ Số tài khoản: 073840887 (ấn để copy)\n"
        "➡️ Tên tài khoản: Le Thi Ngoc Hoa\n\n"
        f"BẮT BUỘC nội dung chuyển là: {deposit_code} (ấn để copy)\n\n"
        "⏳ Mã nạp có hiệu lực 10 phút, chỉ dùng 1 lần.\n\n"
        "🆘 Sau 2-3 phút nếu chưa vào hãy liên hệ CSKH."
    )
    context.bot.send_message(chat_id=user_id, text=msg)

def main():
    TOKEN = os.getenv("BOT_TOKEN")
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("gid", gid))
    dp.add_handler(CommandHandler("nap", nap))
    dp.add_handler(CallbackQueryHandler(handle_callback))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
