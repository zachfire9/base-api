from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
 
class UserModel(db.Model):
    __tablename__ = 'users'
 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    role = db.Column(db.String(80), unique=False)

class LogsModel(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False)
    url = db.Column(db.Text, unique=False)
    headers = db.Column(db.String(64000), unique=False)
    request = db.Column(db.JSON, unique=False)
    response = db.Column(db.JSON, unique=False)