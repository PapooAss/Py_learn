"""
Telegram Bot для включения/выключения режима мута в группе.
Версия: Bot_0.3

Команды:
- /mute: Включает режим мута для всех участников.
- /unmute: Выключает режим мута для всех участников.
- /muted: Показывает список замученных пользователей.

Дополнительные возможности:
- Администратор может снять мут с конкретного пользователя через reply или кнопки.
- Информационные сообщения от бота удаляются через 5 секунд.
- Команды автоматически регистрируются через API при запуске бота.

Требования:
- Бот должен быть администратором в группе.
- Установлена библиотека python-telegram-bot версии 20.x.
"""

from telegram import Update, ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode
from telegram.error import BadRequest
import asyncio

# Функция для проверки, является ли пользователь администратором
async def is_admin(update: Update):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    chat_member = await update.effective_chat.get_member(user_id)
    return chat_member.status in ('administrator', 'creator')

# Удаление сообщения через 5 секунд
async def delete_message(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int):
    await asyncio.sleep(5)
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except BadRequest:
        pass  # Игнорируем ошибку, если сообщение уже удалено

# Обработчик команды /mute
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        msg = await update.message.reply_text("Эта команда доступна только администраторам.")
        await delete_message(context, update.effective_chat.id, msg.message_id)
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
        msg = await update.message.reply_text("Режим мута включен для всех участников.")
        await delete_message(context, chat_id, msg.message_id)
    except BadRequest as e:
        msg = await update.message.reply_text(f"Ошибка: {e.message}")
        await delete_message(context, chat_id, msg.message_id)

# Обработчик команды /unmute
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        msg = await update.message.reply_text("Эта команда доступна только администраторам.")
        await delete_message(context, update.effective_chat.id, msg.message_id)
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
        msg = await update.message.reply_text("Режим мута выключен для всех участников.")
        await delete_message(context, chat_id, msg.message_id)
    except BadRequest as e:
        msg = await update.message.reply_text(f"Ошибка: {e.message}")
        await delete_message(context, chat_id, msg.message_id)

# Обработчик команды /muted
async def muted(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        msg = await update.message.reply_text("Эта команда доступна только администраторам.")
        await delete_message(context, update.effective_chat.id, msg.message_id)
        return

    chat_id = update.effective_chat.id
    members = await context.bot.get_chat_members(chat_id, filter="restricted")

    if not members:
        msg = await update.message.reply_text("Нет замученных пользователей.")
        await delete_message(context, chat_id, msg.message_id)
        return

    message = "Список замученных пользователей:\n"
    for member in members:
        user = member.user
        message += f"- {user.full_name} (@{user.username})\n"

    msg = await update.message.reply_text(message)
    await delete_message(context, chat_id, msg.message_id)

# Обработчик ответа на сообщение
async def handle_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        chat_id = update.effective_chat.id

        # Создаем кнопки
        keyboard = [
            [InlineKeyboardButton("Снять мут", callback_data=f"unmute_{user_id}")],
            [InlineKeyboardButton("Заблокировать", callback_data=f"ban_{user_id}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        msg = await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)
        await delete_message(context, chat_id, msg.message_id)

# Обработчик нажатия кнопки
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, user_id = query.data.split("_")
    user_id = int(user_id)
    chat_id = update.effective_chat.id

    if action == "unmute":
        try:
            await context.bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=ChatPermissions(
                    can_send_messages=True,
                    can_send_polls=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True
                )
            )
            msg = await query.edit_message_text("Мут снят.")
            await delete_message(context, chat_id, msg.message_id)
        except BadRequest as e:
            msg = await query.edit_message_text(f"Ошибка: {e.message}")
            await delete_message(context, chat_id, msg.message_id)
    elif action == "ban":
        try:
            await context.bot.ban_chat_member(chat_id, user_id)
            msg = await query.edit_message_text("Пользователь заблокирован.")
            await delete_message(context, chat_id, msg.message_id)
        except BadRequest as e:
            msg = await query.edit_message_text(f"Ошибка: {e.message}")
            await delete_message(context, chat_id, msg.message_id)

# Основная функция для запуска бота
def main():
    # Замените 'YOUR_BOT_TOKEN' на токен вашего бота
    application = Application.builder().token("8020962158:AAE3xLyQA0Wyvrm-FzpB2tSRgdcTL-h1gvY").build()

    # Регистрация команд через API
    await application.bot.set_my_commands([
        BotCommand("mute", "Включает режим мута для всех участников"),
        BotCommand("unmute", "Выключает режим мута для всех участников"),
        BotCommand("muted", "Показывает список замученных пользователей")
    ])

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("mute", mute))
    application.add_handler(CommandHandler("unmute", unmute))
    application.add_handler(CommandHandler("muted", muted))
    application.add_handler(MessageHandler(None, handle_reply))  # Обработка reply
    application.add_handler(CallbackQueryHandler(button_callback))  # Обработка кнопок

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()