import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram import enums
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Замените на свой токен
BOT_TOKEN = "8165569024:AAEu0BF0wsxfFVw7Y65XxoxmgHEDo6gzENE"

# Учебные материалы (замените на свои)
learning_materials = {
    "Backend developer": {
        "description": "Изучите разработку серверной части веб-приложений.",
        "resources": [
            {"name": "Python Backend Development", "url": "https://example.com/python_backend"},
            {"name": "Node.js Backend Development", "url": "https://example.com/nodejs_backend"}
        ]
    },
    "Frontend developer": {
        "description": "Изучите разработку пользовательского интерфейса веб-приложений.",
        "resources": [
            {"name": "React Tutorial", "url": "https://example.com/react"},
            {"name": "Vue.js Tutorial", "url": "https://example.com/vue"}
        ]
    },
    "CEO": {
        "description": "Материалы для руководителей и предпринимателей.",
        "resources": [
            {"name": "Startup Lessons", "url": "https://example.com/startup"},
            {"name": "Leadership Skills", "url": "https://example.com/leadership"}
        ]
    },
    "Fullstack": {
        "description": "Комплексное обучение веб-разработке.",
        "resources": [
            {"name": "MERN Stack Tutorial", "url": "https://example.com/mern"},
            {"name": "Django Fullstack", "url": "https://example.com/django"}
        ]
    },
    "Data science": {
        "description": "Изучите анализ данных и машинное обучение.",
        "resources": [
            {"name": "Python for Data Science", "url": "https://example.com/datascience"},
            {"name": "Machine Learning Basics", "url": "https://example.com/machinelearning"}
        ]
    }
}

# Кнопка "Назад"
BACK_BUTTON = "Назад"

# Создание главной клавиатуры
main_keyboard = [
    [KeyboardButton(text="Backend developer")],
    [KeyboardButton(text="Frontend developer")],
    [KeyboardButton(text="CEO")],
    [KeyboardButton(text="Fullstack")],
    [KeyboardButton(text="Data science")],
]
main_reply_markup = ReplyKeyboardMarkup(keyboard=main_keyboard, resize_keyboard=True)

# Функция для создания клавиатуры с ресурсами и кнопкой "Назад"
def create_topic_keyboard(topic: str):
    keyboard = []
    for resource in learning_materials[topic]["resources"]:
        keyboard.append([KeyboardButton(text=resource["name"])])  # Кнопки с названиями ресурсов
    keyboard.append([KeyboardButton(text=BACK_BUTTON)])  # Кнопка "Назад"
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Инициализация бота и диспетчера
async def main():
    session = AiohttpSession()
    bot = Bot(BOT_TOKEN, session=session, default=DefaultBotProperties(parse_mode=enums.ParseMode.HTML))
    dp = Dispatcher()

    # Обработчик команды /start
    @dp.message(CommandStart())
    async def start_command(message: types.Message):
        await message.answer("Добро пожаловать! Я – твой личный наставник. Выбери тему:", reply_markup=main_reply_markup)

    # Обработчик текстовых сообщений (кнопки)
    @dp.message(F.text.in_(list(learning_materials.keys())))
    async def learning_topic(message: types.Message):
        topic = message.text
        topic_keyboard = create_topic_keyboard(topic)
        await message.answer(f"<b>{topic}</b>\n\n{learning_materials[topic]['description']}", reply_markup=topic_keyboard)

    # Обработчик кнопки "Назад"
    @dp.message(F.text == BACK_BUTTON)
    async def back_button_handler(message: types.Message):
        await message.answer("Вы вернулись в главное меню.", reply_markup=main_reply_markup)

    # Обработчик ссылок
    @dp.message(F.text.in_([resource["name"] for topic in learning_materials.values() for resource in topic["resources"]]))
    async def resource_button_handler(message: types.Message):
         for topic, data in learning_materials.items():
                for resource in data["resources"]:
                    if resource["name"] == message.text:
                         await message.answer(f"Ссылка на источник: {resource['url']}")
                         return
    # Запуск процесса поллинга
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
