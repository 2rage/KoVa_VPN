import uuid
import requests
import json
import time

# Базовый URL для API
BASE_URL = "http://vpn.2rage.com:65203/2rage"

# Данные для авторизации
USERNAME = "wh/wgnAH"
PASSWORD = "Svc74ecb"


class VPNManager:
    def __init__(self):
        self.session = requests.Session()
        self.session_cookie = None

    def login(self):
        """Авторизация в 3x-ui API для получения сессионной cookie"""
        login_url = f"{BASE_URL}/login"
        data = {"username": USERNAME, "password": PASSWORD}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        # Выполняем запрос на логин
        response = self.session.post(login_url, data=data, headers=headers)

        if response.status_code == 200:
            print("Успешная авторизация!")
            self.session_cookie = response.cookies.get_dict()
        else:
            print(f"Ошибка авторизации {response.status_code}: {response.text}")
            raise Exception("Login failed!")

    def generate_vless_url(
        self,
        client_id,
        domain,
        port,
        flow="xtls-rprx-vision",
        security="reality",
        pbk="fdFiozyLzqjV_xozUSxqsJGxXcuNOpPnCCzhtKapQwg",
        fp="safari",
        sni="yahoo.com",
        sid="bf1f",
        spx="%2F",
        remark="Reality-the2rage",
    ):
        """Генерация VLESS URL на основе данных клиента с дополнительными параметрами"""
        vless_url = f"vless://{client_id}@{domain}:{port}/?type=tcp&security={security}&pbk={pbk}&fp={fp}&sni={sni}&sid={sid}&spx={spx}&flow={flow}#{remark}"
        return vless_url

    def add_client(self, telegram_name, expiry_days=3):
        """Добавление клиента через API с использованием данных Telegram"""
        if not self.session_cookie:
            print("Нет авторизации! Выполняется попытка логина...")
            self.login()

        # URL для добавления клиента
        add_client_url = f"{BASE_URL}/panel/api/inbounds/addClient"

        # Генерируем уникальный ID клиента и подготавливаем данные
        client_id = str(uuid.uuid4())  # Уникальный идентификатор клиента
        current_time = int(time.time()) * 1000  # Текущее время в миллисекундах

        # Формируем данные клиента
        settings = {
            "clients": [
                {
                    "id": client_id,
                    "flow": "xtls-rprx-vision",  # Пример использования XTLS Vision
                    "email": f"{telegram_name}",  # Имя пользователя из Telegram
                    "limitIp": 0,
                    "totalGB": 0,
                    "expiryTime": current_time
                    + (expiry_days * 86400000),  # Время истечения через `expiry_days`
                    "enable": True,
                    "tgId": "",
                    "subId": str(uuid.uuid4()),  # Генерируем subId
                    "reset": 0,
                }
            ]
        }

        # Данные для отправки запроса
        data = {
            "id": "3",  # Пример id (уточни, что означает этот параметр)
            "settings": json.dumps(settings),  # Преобразуем настройки в JSON строку
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        # Отправляем запрос на добавление клиента
        response = self.session.post(
            add_client_url, data=data, cookies=self.session_cookie, headers=headers
        )

        if response.status_code == 200:
            print("Клиент успешно добавлен!")
            # Генерируем VLESS URL на основе данных клиента
            domain = "vpn.2rage.com"
            port = 443
            vless_url = self.generate_vless_url(client_id, domain, port)
            return vless_url
        else:
            print(f"Ошибка добавления клиента {response.status_code}: {response.text}")
            return None
