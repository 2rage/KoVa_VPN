from telegram import Update
from telegram.ext import Application, CommandHandler
from .config import TELEGRAM_TOKEN
from .database import add_user, get_user_by_telegram_id

async def start(update: Update, context):
    """Обрабатываем команду /start и добавляем пользователя в базу данных"""
    telegram_id = update.message.from_user.id
    user = get_user_by_telegram_id(telegram_id)
    
    if not user:
        add_user(telegram_id)
        await update.message.reply_text("Вы были успешно зарегистрированы!")
    else:
        await update.message.reply_text("Вы уже зарегистрированы в системе.")

def main():
    """Основной цикл работы бота"""
    from .database import create_database
    create_database()

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))

    application.run_polling()

if __name__ == "__main__":
    main()
