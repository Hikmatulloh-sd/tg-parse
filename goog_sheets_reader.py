import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

# Авторизация и подключение к Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

# Папка для сохранения файлов
folder_name = "exported_data"
# Проверяем, существует ли папка, если нет — создаём
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Открываем таблицу по её ID
spreadsheet = client.open_by_key('1DoIm9OpYTZqC3bqGaaRQaBD35bBRrumqZYkg_L98uxA')

# Перебираем все листы в таблице
for sheet in spreadsheet.worksheets():
    # Получаем все записи с листа
    data = sheet.get_all_records()

    # Название файла для сохранения данных (с путём к папке)
    filename = os.path.join(folder_name, f"{sheet.title}.json")

    # Записываем данные в JSON файл
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Данные с листа '{sheet.title}' записаны в файл '{filename}'")
