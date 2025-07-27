from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
import os

TOKEN = os.getenv("BOT_TOKEN")  # Lấy token từ biến môi trường trên Render

# Lưu ID game theo user (nhớ: mất khi restart server Free; muốn lưu bền thì dùng DB/Redis)
user_ids = {}

def need_gid_text():
    return ("❗Bạn chưa cài đặt ID Game\n\n"
            "Để cập nhật ID Game cho tài khoản, sử dụng cú pháp:\n"
            "`/gid [dấu cách] ID Game`\n\n"
            "VD: `/gid 123456789`")

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🪙 Nạp tiền", callback_data="nap_tien")],
        [InlineKeyboardButton("🛟 Hỗ trợ", callback_data="ho_tro")],
        [InlineKeyboardButton("🆔 ID Game", callback_data="id_game")],
    ]
    update.message.reply_text("Xin chào! Bạn cần gì?", reply_markup=InlineKeyboardMarkup(keyboard))

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    query.answer()

    if query.data in ("nap_tien", "ngan_hang"):
        if user_id not in user_ids:
            query.edit_message_text(need_gid_text(), parse_mode=ParseMode.MARKDOWN)
            return

    if query.data == "nap_tien":
        query.edit_message_text(
            "Chọn hình thức nạp tiền",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏦 Ngân hàng", callback_data="ngan_hang")]
            ])
        )

    elif query.data == "ngan_hang":
        query.edit_message_text(
            "💸 *Cách nạp tiền qua NGÂN HÀNG (tối thiểu 100k):*\n"
            "➡️ Chuyển tiền vào ngân hàng: *VIB*\n"
            "➡️ Số tài khoản: `073840887`\n"
            "➡️ Tên tài khoản: *Le Thi Ngoc Hoa*\n\n"
            "*BẮT BUỘC nội dung chuyển là:* `DONE5R9AR`\n\n"
            "_Lưu ý : Mã nạp có thời gian trong 10p và chỉ nạp 1 lần. "
            "Để nạp đơn tiếp theo dùng lệnh /nap để lấy lại thông tin Bank và nội dung nạp mới._\n\n"
            "🆘️ Sau 2-3p tiền chưa vào bạn hãy liên hệ CSKH",
            parse_mode=ParseMode.MARKDOWN
        )

    elif query.data == "ho_tro":
        query.edit_message_text(
            "📍 Trung tâm hỗ trợ",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💬 Chat với admin", url="https://t.me/hotro3bett")]
            ])
        )

    elif query.data == "id_game":
        query.edit_message_text(need_gid_text(), parse_mode=ParseMode.MARKDOWN)

def set_gid(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if context.args and context.args[0].isdigit():
        user_ids[user_id] = context.args[0]
        update.message.reply_text("✅ Cập nhật ID Game thành công!")
    else:
        update.message.reply_text("❌ Sai cú pháp. Dùng: /gid 123456789")

def nap(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in user_ids:
        update.message.reply_text(need_gid_text(), parse_mode=ParseMode.MARKDOWN)
        return

    update.message.reply_text(
        "💸 *Thông tin nạp tiền mới:*\n"
        "➡️ Ngân hàng: *VIB*\n➡️ STK: `073840887`\n➡️ Chủ TK: *Le Thi Ngoc Hoa*\n\n"
        "*Nội dung chuyển:* `DONE5R9AR`\n(Mã mới sẽ được tạo nếu là đơn tiếp theo)\n\n"
        "_Lưu ý: Mỗi mã dùng 1 lần trong 10 phút._",
        parse_mode=ParseMode.MARKDOWN
    )

def main():
    if not TOKEN:
        raise RuntimeError("Bạn chưa set biến môi trường BOT_TOKEN trên Render!")
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("gid", set_gid))
    dp.add_handler(CommandHandler("nap", nap))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, start))  # auto hiện menu khi chat text

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
