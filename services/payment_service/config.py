import os

class Config:
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'password')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_DB = os.getenv('MYSQL_DB', 'payment_db')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ORDER_SERVICE_URL = "http://127.0.0.1:5003/"
    STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', 'pk_test_51Pgsh8A8wNkZj8pNzuqOvfmfztMrFje7aMLD4Yyfr6BsXcPUvaGR1HGbrdzBlNKmHq0YTl8k0jWrha9cJsB5xkfT00ISaGCMpl')
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', 'sk_test_51Pgsh8A8wNkZj8pNnIYW8qsy2bdYuM1WAPt62zoUYuaRCtyfPACyfFMyzrh2EoROYn62LzbZvryWeC4TPvOw2UFT0011z34RDW')
