import requests
from .config import Config

# def check_product_availability(artwork_ids):
#     response = requests.post(Config.PRODUCT_SERVICE_URL, json={'artwork_ids': artwork_ids})
#     return response.json()

def check_product_availability(artwork_id, quantity):
    return requests.post(f"{Config.PRODUCT_SERVICE_URL}/check_availability", json={'artwork_id':artwork_id, 'quantity': quantity})

def update_stock(artwork_id, quantity):
    return requests.put(f"{Config.PRODUCT_SERVICE_URL}/artworks/{artwork_id}/update_stock", json={'quantity': quantity})

def get_artwork_by_id(artwork_id):
    return requests.get(f"{Config.PRODUCT_SERVICE_URL}/artworks/{artwork_id}")
