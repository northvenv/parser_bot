import redis
import pandas as pd
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InputFile
from core.parser.parseavito import ParseAvito
import io

API_TOKEN = '5846936280:AAHjdLZUHlJOybPtt93N1UjYkKnmAeBsLWU'  # Замените на ваш токен
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Подключение к Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Функция для парсинга товаров с веб-сайта
def parse_products(text):
    p = ParseAvito
    p.main(text)
    # ваша логика парсинга товаров
    # возвращает данные о товарах

# Функция для создания Excel-файла и сохранения в Redis
def create_and_save_excel(products):
    # создание DataFrame из данных о товарах
    df = pd.DataFrame(products, columns=['Название', 'Ссылка'])
    
    # Запись DataFrame в Excel
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Товары', index=False)
    writer._save()
    output.seek(0)
    
    # Сохранение Excel-файла в Redis
    r.set('excel_file', output.read())

# Отправка Excel-файла пользователю
async def send_excel_to_user(chat_id):
    # Получение Excel-файла из Redis
    excel_file = r.get('excel_file')
    await bot.send_document(chat_id, InputFile(excel_file), caption="Вот файл с товарами")
    # Удаление Excel-файла из Redis
    r.delete('excel_file')

# Обработчик сообщений от пользователей
@dp.message()
async def process_user_message(message: Message):
    chat_id = message.chat.id
    user_text = message.text
    # Парсинг товаров из текста
    parsed_products = parse_products(user_text)
    # Создание и сохранение Excel-файла в Redis
    create_and_save_excel(parsed_products)
    # Отправка Excel-файла пользователю
    await send_excel_to_user(chat_id)
    
async def on_shutdown(dp):
    await bot.session.close()

if __name__ == "__main__":
    dp.start_polling(bot)