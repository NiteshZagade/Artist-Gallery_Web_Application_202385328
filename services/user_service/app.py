from flask import Flask
from .config import Config
from .models import db
from .routes import user_bp
from .login_routes import login_bp
import pymysql
from .auth import configure_jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    jwt = configure_jwt(app)
    app.register_blueprint(user_bp)
    app.register_blueprint(login_bp)    
    return app

def create_database():
    db_user = Config.MYSQL_USER
    db_password = Config.MYSQL_PASSWORD
    db_host = Config.MYSQL_HOST
    db_name = Config.MYSQL_DB

    connection = pymysql.connect(user=db_user, password=db_password, host=db_host)
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    finally:
        connection.close()

def initialize_database(app):
    with app.app_context():
        db.create_all()

# if __name__ == '__main__':
#     create_database()
#     app = create_app()
#     initialize_database(app)
#     app.run(debug=True, port=5001)

create_database()
app = create_app()
initialize_database(app)