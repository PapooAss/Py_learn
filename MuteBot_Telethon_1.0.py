"""
Telegram Bot для включения/выключения режима мута в группе.
Версия: MuteBot_Telethon_6.0

Команды:
- /mute: Включает режим мута для всех участников (кроме администраторов).
- /unmute: Выключает режим мута для всех участников.
- /muted: Показывает список замученных пользователей.

Дополнительные возможности:
- Администратор может снять мут с конкретного пользователя через reply или ключевое слово "голос".
- Информационные сообщения от бота удаляются через 5 секунд.

Требования:
- Установлена библиотека Telethon.
- Используется пользовательский аккаунт Telegram (не бот).
"""

from telethon import TelegramClient, events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from telethon.errors import rpcerrorlist
import asyncio

# Настройки клиента Telethon
api_id = '28648194'  # Замените на ваш API ID
api_hash = 'e528fd294259737d38c60f8a51ee442f'  # Замените на ваш API Hash
client = TelegramClient('session_name', api_id, api_hash)

# Словарь для хранения информации о замученных пользователях
muted_users = {}

# Функция для проверки, является ли пользователь администратором
async def is_admin(chat_id, user_id):
    try:
        participant = await client.get_permissions(chat_id, user_id)
        return participant.is_admin or participant.is_creator
    except Exception as e:
        print(f"Ошибка при проверке прав администратора: {e}")
        return False

# Удаление сообщения через 5 секунд
async def delete_message(chat_id, message_ids):
    await asyncio.sleep(5)
    for message_id in message_ids:
        try:
            await client.delete_messages(chat_id, message_id)
        except Exception:
            pass  # Игнорируем ошибку, если сообщение уже удалено

# Обработчик команды /mute
@client.on(events.NewMessage(pattern='/mute'))
async def mute_handler(event):
    chat_id = event.chat_id
    sender_id = event.sender_id

    # Проверяем, является ли отправитель администратором
    if not await is_admin(chat_id, sender_id):
        msg = await event.reply("Эта команда доступна только администраторам.")
        await delete_message(chat_id, [event.message.id, msg.id])
        return

    try:
        # Получаем всех участников чата
        participants = client.iter_participants(chat_id)  # Используем iter_participants для больших групп
        muted_users[chat_id] = {}

        async for participant in participants:
            user_id = participant.id
            username = participant.username or participant.first_name

            # Пропускаем администраторов
            if await is_admin(chat_id, user_id):
                continue

            # Ограничиваем права отправки сообщений
            await client(EditBannedRequest(
                chat_id,
                user_id,
                ChatBannedRights(
                    until_date=None,  # Блокировка навсегда
                    send_messages=True,  # Запрещаем отправку сообщений
                    send_media=True,  # Запрещаем отправку медиа
                    send_stickers=True,  # Запрещаем отправку стикеров
                    send_gifs=True,  # Запрещаем отправку GIF
                    send_games=True,  # Запрещаем отправку игр
                    send_inline=True,  # Запрещаем отправку inline-запросов
                    embed_links=True  # Запрещаем отправку ссылок
                )
            ))

            # Добавляем пользователя в список замученных
            muted_users[chat_id][user_id] = username

        msg = await event.reply("Режим мута включен для всех участников (кроме администраторов).")
        await delete_message(chat_id, [event.message.id, msg.id])
    except rpcerrorlist.UserAdminInvalidError:
        msg = await event.reply("У бота недостаточно прав для выполнения этой команды.")
        await delete_message(chat_id, [event.message.id, msg.id])

# Обработчик команды /unmute
@client.on(events.NewMessage(pattern='/unmute'))
async def unmute_handler(event):
    chat_id = event.chat_id
    sender_id = event.sender_id

    # Проверяем, является ли отправитель администратором
    if not await is_admin(chat_id, sender_id):
        msg = await event.reply("Эта команда доступна только администраторам.")
        await delete_message(chat_id, [event.message.id, msg.id])
        return

    try:
        # Снимаем мут со всех участников
        if chat_id in muted_users:
            for user_id in muted_users[chat_id]:
                await client(EditBannedRequest(
                    chat_id,
                    user_id,
                    ChatBannedRights(
                        until_date=None,  # Разблокировка
                        send_messages=False,  # Разрешаем отправку сообщений
                        send_media=False,  # Разрешаем отправку медиа
                        send_stickers=False,  # Разрешаем отправку стикеров
                        send_gifs=False,  # Разрешаем отправку GIF
                        send_games=False,  # Разрешаем отправку игр
                        send_inline=False,  # Разрешаем отправку inline-запросов
                        embed_links=False  # Разрешаем отправку ссылок
                    )
                ))

            # Очищаем список замученных пользователей
            muted_users.pop(chat_id)

        msg = await event.reply("Режим мута выключен для всех участников.")
        await delete_message(chat_id, [event.message.id, msg.id])
    except rpcerrorlist.UserAdminInvalidError:
        msg = await event.reply("У бота недостаточно прав для выполнения этой команды.")
        await delete_message(chat_id, [event.message.id, msg.id])

# Обработчик команды /muted
@client.on(events.NewMessage(pattern='/muted'))
async def muted_handler(event):
    chat_id = event.chat_id
    sender_id = event.sender_id

    # Проверяем, является ли отправитель администратором
    if not await is_admin(chat_id, sender_id):
        msg = await event.reply("Эта команда доступна только администраторам.")
        await delete_message(chat_id, [event.message.id, msg.id])
        return

    if not muted_users.get(chat_id):
        msg = await event.reply("Нет пользователей в MUTE")
        await delete_message(chat_id, [event.message.id, msg.id])
        return

    message = "Список пользователей в MUTE:\n"
    for user_id, username in muted_users[chat_id].items():
        message += f"- {username}\n"

    msg = await event.reply(message)
    await delete_message(chat_id, [event.message.id, msg.id])

# Обработчик текстового сообщения для снятия мута по ключевому слову
@client.on(events.NewMessage(func=lambda e: e.text.strip().lower() == "голос"))
async def handle_keyword_unmute(event):
    chat_id = event.chat_id
    sender_id = event.sender_id

    # Проверяем, является ли отправитель администратором
    if not await is_admin(chat_id, sender_id):
        return

    if event.is_reply:
        replied_msg = await event.get_reply_message()
        user_id = replied_msg.sender_id
        username = replied_msg.sender.username or replied_msg.sender.first_name

        # Проверяем, есть ли пользователь в списке замученных
        if chat_id in muted_users and user_id in muted_users[chat_id]:
            try:
                # Восстанавливаем права отправки сообщений
                await client(EditBannedRequest(
                    chat_id,
                    user_id,
                    ChatBannedRights(
                        until_date=None,  # Разблокировка
                        send_messages=False,  # Разрешаем отправку сообщений
                        send_media=False,  # Разрешаем отправку медиа
                        send_stickers=False,  # Разрешаем отправку стикеров
                        send_gifs=False,  # Разрешаем отправку GIF
                        send_games=False,  # Разрешаем отправку игр
                        send_inline=False,  # Разрешаем отправку inline-запросов
                        embed_links=False  # Разрешаем отправку ссылок
                    )
                ))

                # Удаляем пользователя из списка замученных
                del muted_users[chat_id][user_id]

                msg = await event.reply(f"Мут снят с пользователя {username}.")
                await delete_message(chat_id, [event.message.id, msg.id])
            except rpcerrorlist.UserAdminInvalidError:
                msg = await event.reply("У бота недостаточно прав для выполнения этой команды.")
                await delete_message(chat_id, [event.message.id, msg.id])
        else:
            msg = await event.reply(f"Пользователь {username} не находится в муте.")
            await delete_message(chat_id, [event.message.id, msg.id])

# Запуск клиента
if __name__ == '__main__':
    print("Бот запущен. Нажмите Ctrl+C для завершения работы.")
    client.start()
    client.run_until_disconnected()