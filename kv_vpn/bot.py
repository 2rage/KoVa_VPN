from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from .config import TELEGRAM_TOKEN
from .database import add_user, get_user_by_telegram_id
from .messages import START_MESSAGE, MENU_MESSAGE, TEST_DB_SUCCESS, TEST_DB_FAIL, RECOGNIZE_BUTTON, BUY_MESSAGE

# Меню кнопок
def get_main_menu():
    keyboard = [
        ["Купить", "Продлить", "Мои подписки"],
        ["О нас", "Инструкция", "FAQ"],
        ["Тест БД (Не для продакшена)"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Кнопка с редиректом
def get_try_button():
    keyboard = [
        [InlineKeyboardButton("Попробовать за 29₽", url="https://2rage.com")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_buy_options():
    keyboard = [
        [InlineKeyboardButton("Купить на месяц / 149₽", callback_data='buy_1_month')],
        [InlineKeyboardButton("Купить на полгода / 849₽ -5%", callback_data='buy_6_months')],
        [InlineKeyboardButton("Купить на год / 1599₽ -10%", callback_data='buy_1_year')],
        [InlineKeyboardButton("Купить на 3 года / 4599₽ -15%", callback_data='buy_3_years')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context):
    """Обрабатываем команду /start и добавляем пользователя в базу данных"""
    telegram_id = update.message.from_user.id
    user = get_user_by_telegram_id(telegram_id)
    
    # Проверка и добавление пользователя в базу
    if not user:
        add_user(telegram_id)
    
    # Отправка приветственного сообщения с картинкой и кнопкой
    await context.bot.send_photo(
        chat_id=update.message.chat_id,
        photo='https://cliqist.com/wp-content/uploads/2014/07/underdevelopmentlogo.jpg',  # Замените на ссылку или ID вашей картинки
        caption=START_MESSAGE,
        reply_markup=get_try_button()
    )

    # Отправка меню
    await update.message.reply_text(
        MENU_MESSAGE, 
        reply_markup=get_main_menu()
    )

async def handle_message(update: Update, context):
    """Обрабатываем текстовые сообщения с кнопок"""
    text = update.message.text
    telegram_id = update.message.from_user.id

    if text == "Купить":
        # Сообщение и inline-кнопки под сообщением
        await update.message.reply_text(BUY_MESSAGE, reply_markup=get_buy_options())

    elif text == "Тест БД (Не для продакшена)":
        user = get_user_by_telegram_id(telegram_id)
        if user:
            await update.message.reply_text(TEST_DB_SUCCESS)
        else:
            await update.message.reply_text(TEST_DB_FAIL)
    else:
        await update.message.reply_text(RECOGNIZE_BUTTON.format(button_text=text))


def main():
    """Основной цикл работы бота"""
    from .database import create_database
    create_database()

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    
    # Обработчик текстовых сообщений с кнопок
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()

