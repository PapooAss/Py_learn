"""
Telegram Bot для включения/выключения режима мута в группе.
Версия: Bot_1.8

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

# Словарь для хранения информации о замученных пользователях
muted_users = {}

# Функция для проверки, является ли пользователь администратором
async def is_admin(update: Update):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    chat_member = await update.effective_chat.get_member(user_id)
    return chat_member.status in ('administrator', 'creator')

# Удаление сообщения через 5 секунд
async def delete_message(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_ids: list):
    await asyncio.sleep(5)
    for message_id in message_ids:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        except BadRequest:
            pass  # Игнорируем ошибку, если сообщение уже удалено

# Обработчик команды /mute
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        msg = await update.message.reply_text("Эта команда доступна только администраторам.")
        await delete_message(context, update.effective_chat.id, [update.message.message_id, msg.message_id])
        return

    chat_id = update.effective_chat.id
    permissions = ChatPermissions(
        can_send_messages=False
        # can_send_polls=False,
        # can_send_other_messages=False,
        # can_add_web_page_previews=False,
        # can_change_info=False,
        # can_invite_users=False,
        # can_pin_messages=False
    )

    try:
        # Получаем количество участников чата
        member_count = await context.bot.get_chat_member_count(chat_id)

        # Добавляем всех участников (кроме админов) в список замученных
        muted_users[chat_id] = {}
        members = await context.bot.get_chat_administrators(chat_id)
        for member in members:
            if member.status != "administrator" and member.status != "creator":
                user_id = member.user.id
                username = member.user.full_name
                muted_users[chat_id][user_id] = username

        # Устанавливаем ограничения для чата
        await context.bot.set_chat_permissions(chat_id, permissions)
        msg = await update.message.reply_text("Режим мута включен для всех участников.")
        await delete_message(context, chat_id, [update.message.message_id, msg.message_id])
    except BadRequest as e:
        msg = await update.message.reply_text(f"Ошибка: {e.message}")
        await delete_message(context, chat_id, [update.message.message_id, msg.message_id])

# Обработчик команды /unmute
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        msg = await update.message.reply_text("Эта команда доступна только администраторам.")
        await delete_message(context, update.effective_chat.id, [update.message.message_id, msg.message_id])
        return

    chat_id = update.effective_chat.id
    permissions = ChatPermissions(
        can_send_messages=True
        # can_send_polls=True,
        # can_send_other_messages=True,
        # can_add_web_page_previews=True,
        # can_change_info=True,
        # can_invite_users=True,
        # can_pin_messages=True
    )

    try:
        # Снимаем мут со всех участников
        if chat_id in muted_users:
            for user_id in muted_users[chat_id]:
                await context.bot.restrict_chat_member(
                    chat_id=chat_id,
                    user_id=user_id,
                    permissions=permissions
                )
            muted_users.pop(chat_id)  # Очищаем список замученных пользователей

        # Устанавливаем разрешения для чата
        await context.bot.set_chat_permissions(chat_id, permissions)
        msg = await update.message.reply_text("Режим мута выключен для всех участников.")
        await delete_message(context, chat_id, [update.message.message_id, msg.message_id])
    except BadRequest as e:
        msg = await update.message.reply_text(f"Ошибка: {e.message}")
        await delete_message(context, chat_id, [update.message.message_id, msg.message_id])

# Обработчик команды /muted
async def muted(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        msg = await update.message.reply_text("Эта команда доступна только администраторам.")
        await delete_message(context, update.effective_chat.id, [update.message.message_id, msg.message_id])
        return

    chat_id = update.effective_chat.id

    if not muted_users.get(chat_id):
        msg = await update.message.reply_text("Нет пользователей в MUTE")
        await delete_message(context, chat_id, [update.message.message_id, msg.message_id])
        return

    message = "Список пользователей в MUTE:\n"
    for user_id, username in muted_users[chat_id].items():
        message += f"- {username}\n"

    msg = await update.message.reply_text(message)
    await delete_message(context, chat_id, [update.message.message_id, msg.message_id])

# Обработчик текстового сообщения для снятия мута по ключевому слову
async def handle_keyword_unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return

    chat_id = update.effective_chat.id
    message = update.message.text.strip().lower()

    # Ключевое слово для снятия мута
    if message == "голос":
        if update.message.reply_to_message:
            user_id = update.message.reply_to_message.from_user.id
            username = update.message.reply_to_message.from_user.full_name

            # Проверяем, есть ли пользователь в списке замученных
            if chat_id in muted_users and user_id in muted_users[chat_id]:
                # Снимаем мут
                permissions = ChatPermissions(
                    can_send_messages=True
                    # can_send_polls=True,
                    # can_send_other_messages=True,
                    # can_add_web_page_previews=True,
                    # can_change_info=True,
                    # can_invite_users=True,
                    # can_pin_messages=True
                )
                try:
                    await context.bot.restrict_chat_member(
                        chat_id=chat_id,
                        user_id=user_id,
                        permissions=permissions
                    )

                    # Удаляем пользователя из списка замученных
                    del muted_users[chat_id][user_id]

                    msg = await update.message.reply_text(f"Мут снят с пользователя {username}.")
                    await delete_message(context, chat_id, [update.message.message_id, msg.message_id])
                except BadRequest as e:
                    msg = await update.message.reply_text(f"Ошибка: {e.message}")
                    await delete_message(context, chat_id, [update.message.message_id, msg.message_id])
            else:
                msg = await update.message.reply_text(f"Пользователь {username} не находится в муте.")
                await delete_message(context, chat_id, [update.message.message_id, msg.message_id])

# Основная функция для запуска бота
async def main():
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
    application.add_handler(CommandHandler("muted", muted))  # <<< ИСПРАВЛЕНО
    application.add_handler(MessageHandler(None, handle_keyword_unmute))  # Обработка ключевого слова

    # Запускаем бота
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    # Бесконечный цикл для поддержания работы бота
    print("Бот запущен. Нажмите Ctrl+C для завершения работы.")
    while True:
        await asyncio.sleep(1)  # Ждем 1 секунду перед следующей итерацией

if __name__ == '__main__':
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")