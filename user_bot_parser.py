import os
import re
import time
import random
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
channel_usernames = [
    "Nargilya_Soul", "channel2", "channel3", "channel4", "channel5", 
    "channel6", "channel7", "channel8", "channel9", "channel10", "channel11"
]  # список каналов для проверки

# Функция для обработки канала с паузой в случае FLOOD_WAIT
def parse_channel(channel_username, request_count):
    try:
        chat = app.get_chat(channel_username)
        description = chat.description or ""
        contacts = CONTACT_REGEX.findall(description)
        
        print(f"Название канала: {chat.title}")
        print(f"Контакты, найденные в описании: {contacts if contacts else 'Контакты не найдены'}")
        return contacts
    except Exception as e:
        if "FLOOD_WAIT" in str(e):
            wait_time = int(re.search(r'(\d+)', str(e)).group(1))
            print(f"Необходимо подождать {wait_time} секунд...")
            time.sleep(wait_time)  # Ждём, если произошла ошибка FLOOD_WAIT
            return parse_channel(channel_username, request_count)  # Повторяем запрос
        else:
            print(f"Ошибка при парсинге канала {channel_username}: {e}")
            return None

# Основная функция для обработки списка каналов с ограничением на 10 запросов
def parse_channels():
    request_count = 0  # Счётчик запросов
    for channel_username in channel_usernames:
        if request_count >= 10:  # Ограничиваем до 10 запросов
            print("Достигнут лимит запросов (10). Завершаем выполнение.")
            break
        print(f"Обработка канала: {channel_username}")
        with app:
            parse_channel(channel_username, request_count)
        
        # Случайная пауза между запросами от 10 до 20 секунд
        random_pause = random.randint(10, 20)
        print(f"Пауза {random_pause} секунд перед следующим запросом...")
        time.sleep(random_pause)
        
        request_count += 1

# Запуск парсинга
parse_channels()
