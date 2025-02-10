from telegram import Update, ChatPermissions
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import BadRequest

# Функция для проверки, является ли пользователь администратором
async def is_admin(update: Update):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    chat_member = await update.effective_chat.get_member(user_id)
    return chat_member.status in ('administrator', 'creator')

# Обработчик команды /mute
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text("Эта команда доступна только администраторам.")
        return

    chat_id = update.effective_chat.id
    permissions = ChatPermissions(
        can_send_messages=False,
        can_send_polls=False,
        can_send_other_messages=False,
        can_add_web_page_previews=False,
        can_change_info=False,
        can_invite_users=False,
        can_pin_messages=False
    )

    try:
        await context.bot.set_chat_permissions(chat_id, permissions)
        await update.message.reply_text("Режим мута включен для всех участников.")
    except BadRequest as e:
        await update.message.reply_text(f"Ошибка: {e.message}")

# Обработчик команды /unmute
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text("Эта команда доступна только администраторам.")
        return

    chat_id = update.effective_chat.id
    permissions = ChatPermissions(
        can_send_messages=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
        can_change_info=True,
        can_invite_users=True,
        can_pin_messages=True
    )

    try:
        await context.bot.set_chat_permissions(chat_id, permissions)
        await update.message.reply_text("Режим мута выключен для всех участников.")
    except BadRequest as e:
        await update.message.reply_text(f"Ошибка: {e.message}")

# Основная функция для запуска бота
def main():
    # Замените 'YOUR_BOT_TOKEN' на токен вашего бота
    application = Application.builder().token("8020962158:AAE3xLyQA0Wyvrm-FzpB2tSRgdcTL-h1gvY").build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("mute", mute))
    application.add_handler(CommandHandler("unmute", unmute))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()