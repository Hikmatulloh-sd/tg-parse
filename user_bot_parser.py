import os
import re
import time
import json
import random
from pyrogram import Client
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

# Подключение к Telegram
app = Client("my_account", api_id=api_id, api_hash=api_hash)

# Регулярка для поиска username или ссылок на Telegram
CONTACT_REGEX = re.compile(r'@[\w\d_]+|t\.me/[\w\d_]+|https://t\.me/[\w\d_]+', re.IGNORECASE)

# Путь к папке с JSON-файлами
EXPORT_PATH = "exported_data"

def extract_contacts(channel_username: str):
    """Получение контактов из описания канала"""
    try:
        chat = app.get_chat(channel_username)
        description = chat.description or ""
        contacts = CONTACT_REGEX.findall(description)
        print(f"📦 {channel_username} → Найдено контактов: {contacts}")
        return ", ".join(contacts) if contacts else ""
    except Exception as e:
        if "FLOOD_WAIT" in str(e):
            wait_time = int(re.search(r'(\d+)', str(e)).group(1))
            print(f"⏳ FLOOD_WAIT: ждём {wait_time} секунд...")
            time.sleep(wait_time)
            return extract_contacts(channel_username)
        else:
            print(f"❌ Ошибка при парсинге '{channel_username}': {e}")
            return ""

def process_file(filepath):
    """Обработка одного JSON-файла"""
    print(f"\n📂 Обработка файла: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    for entry in data:
        username = entry.get("Ник канала")
        if username:
            contacts = extract_contacts(username)
            entry["Автор (ник ссылка)"] = contacts
            pause = random.randint(10, 20)
            print(f"🕒 Пауза {pause} секунд...\n")
            time.sleep(pause)

    # Перезапись файла
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    app.start()
    try:
        files = [f for f in os.listdir(EXPORT_PATH) if f.endswith(".json")]
        for file in files:
            process_file(os.path.join(EXPORT_PATH, file))
        print("\n✅ Завершено.")
    finally:
        app.stop()

if __name__ == "__main__":
    main()
