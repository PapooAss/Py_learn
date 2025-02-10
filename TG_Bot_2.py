import logging
from telegram import Update, ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
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
        self.selecting_users = False  # Флаг выбора пользователей
        self.selected_users = []  # Временный список выбранных пользователей

bot_state = BotState()

# Команда для администратора: начать выбор пользователей
async def start_user_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    bot_state.selecting_users = True
    bot_state.selected_users = []

    # Получаем список администраторов чата
    administrators = await context.bot.get_chat_administrators(chat_id)

    # Создаем клавиатуру с кнопками для выбора пользователей
    keyboard = [
        [InlineKeyboardButton(f"{admin.user.full_name}", callback_data=f"select_{admin.user.id}")]
        for admin in administrators
    ]
    keyboard.append([InlineKeyboardButton("Подтвердить выбор", callback_data="confirm")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Выберите минимум двух пользователей, которым разрешено писать:", reply_markup=reply_markup)

# Обработка нажатия на кнопки
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "confirm":
        # Подтверждение выбора
        if len(bot_state.selected_users) < 2:
            await query.edit_message_text("Необходимо выбрать как минимум двух пользователей!")
            return

        bot_state.allowed_users = bot_state.selected_users
        bot_state.is_active = True
        bot_state.selecting_users = False

        # Ограничиваем права всех участников чата
        await restrict_chat_members(query.message.chat_id, context)

        # Запускаем таймер на 5 минут
        bot_state.timer_task = asyncio.create_task(timer_task(query.message.chat_id, context))

        await query.edit_message_text(f"Режим активирован! Разрешено писать пользователям с ID: {', '.join(map(str, bot_state.allowed_users))}")
    elif data.startswith("select_"):
        # Выбор пользователя
        user_id = int(data.split("_")[1])
        if user_id in bot_state.selected_users:
            bot_state.selected_users.remove(user_id)
            await query.edit_message_text("Пользователь удален из выбора.")
        else:
            bot_state.selected_users.append(user_id)
            await query.edit_message_text("Пользователь добавлен в выбор.")

# Ограничение прав участников чата
async def restrict_chat_members(chat_id, context):
    permissions = ChatPermissions(can_send_messages=False)
    async for member in context.bot.get_chat_members(chat_id):
        user_id = member.user.id
        if user_id not in bot_state.allowed_users:
            await context.bot.restrict_chat_member(chat_id, user_id, permissions)

# Таймер на 5 минут
async def timer_task(chat_id, context):
    for i in range(5, 0, -1):
        await context.bot.send_message(chat_id, f"До конца режима осталось {i} минут.")
        await asyncio.sleep(60)

    # По истечении времени удаляем все сообщения и снимаем ограничения
    await cleanup_and_reset(chat_id, context)

# Очистка чата и сброс состояния
async def cleanup_and_reset(chat_id, context):
    # Удаляем все сообщения за время действия режима
    async for message in context.bot.get_chat(chat_id).iter_history():
        await message.delete()

    # Возвращаем всем право писать сообщения
    permissions = ChatPermissions(can_send_messages=True)
    async for member in context.bot.get_chat_members(chat_id):
        await context.bot.restrict_chat_member(chat_id, member.user.id, permissions)

    # Сбрасываем состояние бота
    bot_state.is_active = False
    bot_state.allowed_users = []
    bot_state.timer_task = None

    await context.bot.send_message(chat_id, "Режим завершен. Все сообщения удалены.")

# Обработка команды "Стоп"
async def stop_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    # Проверяем, есть ли право у пользователя остановить режим
    if user_id in bot_state.allowed_users and bot_state.is_active:
        if bot_state.timer_task:
            bot_state.timer_task.cancel()

        await cleanup_and_reset(chat_id, context)
        await update.message.reply_text("Режим остановлен администратором.")

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
    application.add_handler(CommandHandler("start_mode", start_user_selection))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(CommandHandler("stop", stop_mode))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()