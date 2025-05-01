import os
import re
from pyrogram import Client
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

# Подключение к Telegram
app = Client("my_account", api_id=api_id, api_hash=api_hash)

# Регулярка для поиска контактов в описании канала
CONTACT_REGEX = re.compile(r'@[\w\d_]+|t\.me/[\w\d_]+|https://t\.me/[\w\d_]+', re.IGNORECASE)

# Пример: username или ссылка канала
channel_username = "Nargilya_Soul"  # без @

with app:
    try:
        chat = app.get_chat(channel_username)
        description = chat.description or ""
        contacts = CONTACT_REGEX.findall(description)

        print(f"Название канала: {chat.title}")
        print(f"Контакты, найденные в описании: {contacts if contacts else 'Контакты не найдены'}")
    except Exception as e:
        print(f"Ошибка: {e}")
