from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from .config import TELEGRAM_TOKEN
from .database import add_user, get_user_by_telegram_id

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
        caption=("Привет! Это частный бот KoVa VPN\n\n"
                 "Нажмите на необходимую кнопку из меню ниже ⬇️\n\n"
                 "Вы также можете испытать пробную версию на месяц за 29₽ "
                 "по быстрой ссылке ниже ⬇️"),
        reply_markup=get_try_button()
    )

    # Отправка меню
    await update.message.reply_text(
        "Выберите нужную опцию из меню:", 
        reply_markup=get_main_menu()
    )

async def handle_message(update: Update, context):
    """Обрабатываем текстовые сообщения с кнопок"""
    text = update.message.text
    telegram_id = update.message.from_user.id

    if text == "Тест БД (Не для продакшена)":
        user = get_user_by_telegram_id(telegram_id)
        if user:
            await update.message.reply_text("Пользователь найден в базе данных.")
        else:
            await update.message.reply_text("Пользователь не найден в базе данных.")
    else:
        await update.message.reply_text(f"Вы нажали кнопку: {text}")


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

