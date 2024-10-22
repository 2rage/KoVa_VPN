from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from .config import TELEGRAM_TOKEN
from .database import add_user, get_user_by_telegram_id, update_vpn_config_created
from .messages import (
    START_MESSAGE,
    MENU_MESSAGE,
    TEST_DB_SUCCESS,
    TEST_DB_FAIL,
    RECOGNIZE_BUTTON,
    BUY_MESSAGE,
)
from .vpn_manager import VPNManager  # Импорт VPN Manager

# Инициализация VPN Manager
vpn_manager = VPNManager()


# Меню кнопок
def get_main_menu():
    keyboard = [
        ["Купить", "Продлить", "Мои подписки"],
        ["О нас", "Инструкция", "FAQ"],
        ["Тест БД (Не для продакшена)"],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# Кнопка с редиректом и inline кнопка для создания VPN-конфига
def get_try_button():
    keyboard = [
        [
            InlineKeyboardButton("Попробовать за 29₽", callback_data="try_vpn")
        ]  # callback вместо URL
    ]
    return InlineKeyboardMarkup(keyboard)


def get_buy_options():
    keyboard = [
        [InlineKeyboardButton("Купить на месяц / 149₽", callback_data="buy_1_month")],
        [
            InlineKeyboardButton(
                "Купить на полгода / 849₽ -5%", callback_data="buy_6_months"
            )
        ],
        [
            InlineKeyboardButton(
                "Купить на год / 1599₽ -10%", callback_data="buy_1_year"
            )
        ],
        [
            InlineKeyboardButton(
                "Купить на 3 года / 4599₽ -15%", callback_data="buy_3_years"
            )
        ],
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
        photo="https://cliqist.com/wp-content/uploads/2014/07/underdevelopmentlogo.jpg",  # Замените на ссылку или ID вашей картинки
        caption=START_MESSAGE,
        reply_markup=get_try_button(),  # Добавляем кнопку для создания VPN-конфига
    )

    # Отправка меню
    await update.message.reply_text(MENU_MESSAGE, reply_markup=get_main_menu())


# Обработчик нажатия на кнопку "Попробовать за 29₽"
async def try_vpn_callback(update: Update, context):
    """Обрабатываем нажатие на кнопку 'Попробовать за 29₽' и создаем VPN-конфиг"""
    query = update.callback_query
    await query.answer()

    telegram_id = query.from_user.id
    telegram_name = query.from_user.username

    user = get_user_by_telegram_id(telegram_id)

    if user.vpn_config_created:
        await query.message.reply_text(
            "Вы уже создавали пробный VPN-конфиг. Повторное создание невозможно."
        )
    else:
        # Создаем VPN-конфиг через API
        result = vpn_manager.add_client(telegram_name)

        # Проверяем успешность
        if result:
            # Обновляем статус в базе данных, что конфиг был создан
            update_vpn_config_created(user)
            await query.message.reply_text(
                f"Конфиг для {telegram_name} успешно создан на 3 дня!"
            )
        else:
            await query.message.reply_text(
                "Не удалось создать конфиг, попробуйте позже."
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
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    # Обработчик для нажатия на кнопку "Попробовать за 29₽"
    application.add_handler(CallbackQueryHandler(try_vpn_callback, pattern="try_vpn"))

    application.run_polling()


if __name__ == "__main__":
    main()
