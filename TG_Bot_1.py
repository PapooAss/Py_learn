from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я ваш первый бот.")

# Функция для обработки текстовых сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text(f"Вы сказали: {user_message}")

# Основная функция для запуска бота
def main():
    # Замените 'YOUR_TOKEN' на токен вашего бота
    application = Application.builder().token("928286591:AAGEeQwH6Co1EHwC4HmDZVoNQovxiD-KPt8").build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запуск бота
    print("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()