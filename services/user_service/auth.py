from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import datetime

def configure_jwt(app):
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    jwt = JWTManager(app)
    return jwt

def create_token(identity):
    expires = datetime.timedelta(days=1)
    return create_access_token(identity=identity, expires_delta=expires)

def protect_route(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper
