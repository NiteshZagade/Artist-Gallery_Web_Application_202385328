import requests
from .config import Config

def get_cart_by_user(created_by):
    return requests.get(f"{Config.ORDER_SERVICE_URL}/cart/{created_by}")