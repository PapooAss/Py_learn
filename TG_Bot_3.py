import logging
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telethon import TelegramClient
import asyncio

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Состояние бота
class BotState:
    def __init__(self):
        self.is_active = False  # Флаг активности режима
        self.allowed_users = []  # Список пользователей, которым разрешено писать
        self.timer_task = None   # Задача таймера
        self.waiting_for_user = False  # Флаг ожидания ввода пользователя для /addvoice

bot_state = BotState()

# Настройка Telethon
api_id = '28648194'  # Замените на ваш API ID
api_hash = 'e528fd294259737d38c60f8a51ee442f'  # Замените на ваш API Hash
telethon_client = TelegramClient('session_name', api_id, api_hash)

async def get_all_chat_members(chat_id):
    async with telethon_client:
        participants = await telethon_client.get_participants(chat_id)
        return participants

# Команда для администратора: включить общий мут
async def start_mute_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    # Проверяем, является ли пользователь администратором
    try:
        chat_member = await context.bot.get_chat_member(chat_id, user_id)
        if chat_member.status not in ['creator', 'administrator']:
            await update.message.reply_text("У вас нет прав для выполнения этой команды.")
            return
    except Exception as e:
        logger.error(f"Ошибка при проверке прав администратора: {e}")
        await update.message.reply_text("Произошла ошибка при проверке прав. Убедитесь, что бот является администратором чата.")
        return

    bot_state.is_active = True

    # Ограничиваем права всех участников чата
    await restrict_chat_members(chat_id, context)

    # Запускаем таймер на 5 минут
    bot_state.timer_task = asyncio.create_task(timer_task(chat_id, context))

    await update.message.reply_text("Общий мут активирован! Все участники лишены права писать сообщения на 5 минут.")

# Команда для администратора: выключить мут
async def unmute_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    # Проверяем, является ли пользователь администратором
    try:
        chat_member = await context.bot.get_chat_member(chat_id, user_id)
        if chat_member.status not in ['creator', 'administrator']:
            await update.message.reply_text("У вас нет прав для выполнения этой команды.")
            return
    except Exception as e:
        logger.error(f"Ошибка при проверке прав администратора: {e}")
        await update.message.reply_text("Произошла ошибка при проверке прав. Убедитесь, что бот является администратором чата.")
        return

    # Останавливаем таймер, если он запущен
    if bot_state.timer_task:
        bot_state.timer_task.cancel()

    # Восстанавливаем права всех участников
    await cleanup_and_reset(chat_id, context)

    await update.message.reply_text("Режим мута отключен. Всем возвращено право писать.")

# Обработка команды /addvoice
async def add_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    # Проверяем, является ли пользователь администратором
    try:
        chat_member = await context.bot.get_chat_member(chat_id, user_id)
        if chat_member.status not in ['creator', 'administrator']:
            await update.message.reply_text("У вас нет прав для выполнения этой команды.")
            return
    except Exception as e:
        logger.error(f"Ошибка при проверке прав администратора: {e}")
        await update.message.reply_text("Произошла ошибка при проверке прав. Убедитесь, что бот является администратором чата.")
        return

    # Проверяем, активен ли режим мута
    if not bot_state.is_active:
        await update.message.reply_text("Режим мута не активен. Используйте команду /mute для его активации.")
        return

    # Устанавливаем флаг ожидания ввода пользователя
    bot_state.waiting_for_user = True
    await update.message.reply_text("Укажите ID или полное имя пользователя, чтобы предоставить ему право голоса.")

# Обработка сообщений для /addvoice
async def handle_add_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not bot_state.waiting_for_user:
        return

    # Получаем текст сообщения
    message_text = update.message.text
    chat_id = update.message.chat_id

    # Проверяем, что сообщение содержит ID или имя пользователя
    try:
        user_id = int(message_text)  # Если указан ID
    except ValueError:
        # Если указано имя пользователя
        members = await get_all_chat_members(chat_id)
        user_id = None
        for member in members:
            if member.first_name.lower() == message_text.lower() or member.last_name.lower() == message_text.lower():
                user_id = member.id
                break

        if not user_id:
            await update.message.reply_text("Пользователь не найден. Укажите корректный ID или полное имя.")
            return

    try:
        # Получаем информацию о пользователе по ID
        user = await context.bot.get_chat_member(chat_id, user_id)
        full_name = user.user.full_name

        # Добавляем пользователя в список разрешенных
        if user_id not in bot_state.allowed_users:
            bot_state.allowed_users.append(user_id)
            await context.bot.restrict_chat_member(
                chat_id,
                user_id,
                ChatPermissions(can_send_messages=True)
            )
            await update.message.reply_text(f"Пользователь {full_name} получил право голоса!")
        else:
            await update.message.reply_text(f"Пользователь {full_name} уже имеет право голоса.")
    except Exception as e:
        logger.error(f"Ошибка при добавлении пользователя: {e}")
        await update.message.reply_text("Не удалось найти указанного пользователя. Убедитесь, что он находится в чате.")

    # Сбрасываем флаг ожидания ввода
    bot_state.waiting_for_user = False

# Ограничение прав участников чата
async def restrict_chat_members(chat_id, context):
    permissions = ChatPermissions(can_send_messages=False)

    # Получаем список всех участников чата через Telethon
    members = await get_all_chat_members(chat_id)
    for member in members:
        user_id = member.id

        # Проверяем, является ли участник владельцем или администратором
        try:
            chat_member = await context.bot.get_chat_member(chat_id, user_id)
            if chat_member.status in ['creator', 'administrator']:
                continue  # Пропускаем владельца и администраторов
        except Exception as e:
            logger.error(f"Ошибка при проверке статуса участника {user_id}: {e}")
            continue

        # Применяем ограничения, если участник не в списке разрешенных
        if user_id not in bot_state.allowed_users:
            try:
                await context.bot.restrict_chat_member(chat_id, user_id, permissions)
            except Exception as e:
                logger.error(f"Ошибка при ограничении участника {user_id}: {e}")

# Таймер на 5 минут
async def timer_task(chat_id, context):
    for i in range(5, 0, -1):
        await context.bot.send_message(chat_id, f"До конца режима мута осталось {i} минут.")
        await asyncio.sleep(60)

    # По истечении времени снимаем ограничения
    await cleanup_and_reset(chat_id, context)

# Очистка чата и сброс состояния
async def cleanup_and_reset(chat_id, context):
    # Возвращаем всем право писать сообщения
    permissions = ChatPermissions(can_send_messages=True)
    async for member in context.bot.get_chat_members(chat_id):
        try:
            await context.bot.restrict_chat_member(chat_id, member.user.id, permissions)
        except Exception as e:
            logger.error(f"Ошибка при восстановлении прав участника {member.user.id}: {e}")

    # Сбрасываем состояние бота
    bot_state.is_active = False
    bot_state.allowed_users = []
    bot_state.timer_task = None

    await context.bot.send_message(chat_id, "Режим мута завершен. Всем возвращено право писать.")

# Обработка любых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    # Если режим активен и пользователь не в списке разрешенных
    if bot_state.is_active and user_id not in bot_state.allowed_users:
        await update.message.delete()

# Основная функция
def main():
    token = "8020962158:AAE3xLyQA0Wyvrm-FzpB2tSRgdcTL-h1gvY"  # Замените на токен вашего бота

    application = ApplicationBuilder().token(token).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("mute", start_mute_mode))
    application.add_handler(CommandHandler("unmute", unmute_chat))
    application.add_handler(CommandHandler("addvoice", add_voice))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_add_voice_message))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()