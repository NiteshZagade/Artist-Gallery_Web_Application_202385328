from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enums import UserTypeEnum
from utils import format_datetime, get_enum_value, generate_unique_id

db = SQLAlchemy()
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), nullable=True)
    fname = db.Column(db.String(80), nullable=True)
    lname = db.Column(db.String(80), nullable=True)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    isactive = db.Column(db.Boolean, nullable=False)
    user_type = db.Column(db.Integer, nullable=False)
    failed_login_attempts = db.Column(db.Integer, default=False)
    last_failed_login_attempt_on = db.Column(db.DateTime, nullable=True, onupdate=datetime.today())
    account_locked = db.Column(db.Boolean, default=False)
    account_locked_on = db.Column(db.DateTime, nullable=True, onupdate=datetime.today())
    created_on = db.Column(db.DateTime, default=datetime.today())
    modified_on = db.Column(db.DateTime, default=datetime.today(), onupdate=datetime.today())
    
    @property
    def get_user_type_string(self):
        # Reverse mapping to get the string value from the stored integer        
        return UserTypeEnum.reverse_mapping()[self.user_type]
    
    @staticmethod
    def get_user_type_value(user_type_string):
        return get_enum_value(UserTypeEnum, user_type_string)

    @property
    def formatted_created_on(self):
        return format_datetime(self.created_on)

    @property
    def formatted_modified_on(self):
        return format_datetime(self.modified_on)
    
    def to_dic(self):
        return {
                    'id': self.id,
                    'fname': self.fname,
                    'lname': self.lname,
                    'username': self.username,
                    'email': self.email,
                    'isactive': self.isactive,
                    'usertype': self.user_type,
                    'usertype_string': self.get_user_type_string,
                    'created_on': self.formatted_created_on,
                    'modified_on': self.formatted_modified_on if self.modified_on else None
                }
    
def before_insert_listener(mapper, connection, target):
    last_user = User.query.order_by(User.id.desc()).first()
    target.user_id = generate_unique_id(last_user, 'USR')

# event added to run before_insert_listener
from sqlalchemy import event
event.listen(User, 'before_insert', before_insert_listener)