from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from .yoomoney import check_payment
from .vpn_manager import create_vpn_config
from .database import get_user_by_telegram_id, add_user, set_vpn_config, set_subscription_expiration, update_balance
from .config import TELEGRAM_TOKEN, SUBSCRIPTION_COST
import datetime


reply_keyboard = [['Подписка', 'Баланс']]


markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

async def start(update: Update, context):
    telegram_id = str(update.message.from_user.id)

    user = get_user_by_telegram_id(telegram_id)
    if not user:
        add_user(telegram_id)
        await update.message.reply_text("Привет! Вы добавлены в систему. Нажми кнопку для подписки или проверки баланса.", reply_markup=markup)
    else:
        await update.message.reply_text("С возвращением! Нажми кнопку для подписки или проверки баланса.", reply_markup=markup)

async def subscribe(update: Update, context):
    telegram_id = str(update.message.from_user.id)
    user = get_user_by_telegram_id(telegram_id)

    # Проверка оплаты и активации VPN
    if check_payment(telegram_id):
        config = create_vpn_config(telegram_id)
        if config:
            set_vpn_config(user, config)
            expiration = datetime.datetime.now() + datetime.timedelta(days=30)
            set_subscription_expiration(user, expiration)
            await update.message.reply_text(f"Ваш VPN конфиг: {config}. Подписка активна до {expiration}.")
        else:
            await update.message.reply_text("Ошибка при создании VPN конфига.")
    else:
        await update.message.reply_text(f"Недостаточно средств. Стоимость подписки: {SUBSCRIPTION_COST} рублей.")

async def balance(update: Update, context):
    telegram_id = str(update.message.from_user.id)
    user = get_user_by_telegram_id(telegram_id)

    # Показываем баланс пользователя
    await update.message.reply_text(f"Ваш баланс: {user.balance} рублей.")

def main():
    # Инициализируем базу данных (создаем таблицы, если их нет)
    from .database import create_database
    create_database()

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    
    # Обработчик сообщений с кнопками
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()
