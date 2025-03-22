import logging
import requests 
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

keyboard = [
    [KeyboardButton("Backend devoloper")],
    [KeyboardButton("Frontend devoloper")],
    [KeyboardButton("CEO")],
    [KeyboardButton("Fullstack")],
    [KeyboardButton("Data science")],
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Функция для обработки текстовых сообщений (при нажатии на кнопки)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    if text == "Backend devoloper":
        await update.message.reply_text("Backend devoloper")
    elif text == "Frontend devoloper":
        await update.message.reply_text("Frontend devoloper")
    elif text == "CEO":
        await update.message.reply_text("CEO")
    elif text == "Fullstack":
        await update.message.reply_text("Fullstack")
    elif text == "Data science":
        await update.message.reply_text("Data science")
    else:
        await update.message.reply_text("Я не понимаю эту команду.")

# Функция для отправки клавиатуры при запуске бота
async def post_init(application: ApplicationBuilder) -> None:
    await application.bot.set_my_commands([])  # Убираем команды
    image_url = "https://img.lovepik.com/png/20231112/cartoon-smart-person-pointing-with-glasses-sticker-vector-clipart-arm_572635_wh860.png"  # Замените на URL вашей картинки
    try:
        # Отправляем картинку
        with open(image_path, 'rb') as photo_file:
            await application.bot.send_photo(chat_id=286683463, 
                                            photo=photo_file,
                                            caption="Добро пожаловать! Я – твой личный наставник в безграничном мире информации. Моя цель – помочь тебе раскрыть свой потенциал и получить новые знания легко и с удовольствием. Просто выбери интересующую тебя тему, и я направлю тебя на путь успеха!",
                                            reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Ошибка при отправке картинки: {e}")
if __name__ == '__main__':
    # Вставьте свой токен
    app = ApplicationBuilder().token("8165569024:AAEu0BF0wsxfFVw7Y65XxoxmgHEDo6gzENE").post_init(post_init).build()

    # Регистрация обработчика текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    app.run_polling()
