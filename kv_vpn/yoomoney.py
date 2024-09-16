import requests
from .config import YOOMONEY_TOKEN

def check_payment(user_id):
    # Проверяем успешные платежи пользователя через YooMoney API
    url = f"https://yoomoney.ru/api/check-payment?user_id={user_id}"
    headers = {
        "Authorization": f"Bearer {YOOMONEY_TOKEN}",
    }
    response = requests.get(url, headers=headers)
    # Простая проверка (добавь логику в зависимости от API YooMoney)
    return response.json().get("paid", False)
