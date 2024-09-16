import os

TELEGRAM_TOKEN = 'your-telegram-bot-token'
DATABASE_URL = 'postgresql://username:password@localhost:5432/vpn_bot_db'
# DATABASE_URL = 'postgresql://username:password@localhost:5432/vpn_bot_db'
# TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "your_telegram_bot_token")
YOOMONEY_TOKEN = os.getenv("YOOMONEY_TOKEN", "your_yoomoney_api_key")
VPN_API_URL = os.getenv("VPN_API_URL", "https://your-vpn-server.com/api")
VPN_API_KEY = os.getenv("VPN_API_KEY", "your_vpn_api_key")
SUBSCRIPTION_COST = 300  # Стоимость подписки в рублях
