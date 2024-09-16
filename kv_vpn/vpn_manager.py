import requests
from .config import VPN_API_URL, VPN_API_KEY

def create_vpn_config(user_id: str):
    url = f"{VPN_API_URL}/create"
    headers = {"Authorization": f"Bearer {VPN_API_KEY}"}
    data = {"user_id": user_id}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json().get("config")
    return None

def delete_vpn_config(user_id: str):
    url = f"{VPN_API_URL}/delete"
    headers = {"Authorization": f"Bearer {VPN_API_KEY}"}
    data = {"user_id": user_id}
    response = requests.post(url, json=data, headers=headers)
    return response.status_code == 200
