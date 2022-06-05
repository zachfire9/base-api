import base64
import hashlib
import jwt
import logging
import logging.config
import os
import yaml

from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, request, abort, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from models import db, LogsModel, UserModel

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
limiter = Limiter(app, key_func=get_remote_address)

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

app.logger.setLevel(logging.DEBUG)

@app.before_request
def log_request_info():
    app.logger.debug('Request URL: %s', request.url)

    sanitized_headers = ''
    for key, val in request.headers:
        if key != 'X-Access-Token':
            sanitized_headers += f'{key}: {val}\n'

    app.logger.debug('Request Headers: %s', str(sanitized_headers))

    request_body = request.get_data()
    if request.path.startswith('/login'):
        request_body = 'REDACTED'

    app.logger.debug('Request Body: %s', request_body)

def authenticate(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')

        if not token:
            return jsonify(error="Token is required for every request"), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user = UserModel.query.get(data['id'])
        except:
            return jsonify(error="Invalid login"), 401

        if not user or user.role != 'admin':
            return jsonify(error="Invalid login"), 401

        return  f(user, *args, **kwargs)

    return decorated

@app.route("/", methods = ['POST', 'GET'])
@limiter.limit("10/minute")
def index():
    return jsonify(error="Route not implemented"), 501

@app.route('/login', methods =['POST'])
@limiter.limit("10/minute")
def login():
    email = request.get_json().get('email')
    password = request.get_json().get('password')
    encrypted_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    if not email and password:
        return jsonify(error="Login value(s) missing"), 401

    user = UserModel.query.filter_by(email = email, role = 'admin').first()

    if not user or user.password != encrypted_password:
        return jsonify(error="Invalid login"), 401

    token = jwt.encode({
        'id': user.id,
        'role': user.role,
        'exp' : datetime.utcnow() + timedelta(minutes = 30)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return {
        'token': token
    }


@app.route("/users", methods = ['POST'])
@authenticate
@limiter.limit("10/minute")
def users(user):
    user_email = request.get_json().get('email')
    user_password = request.get_json().get('password')

    user_email = request.get_json().get('email')
    if not user_email:
        return jsonify(error="Missing email"), 400

    user_password = request.get_json().get('password')
    if not user_password:
        return jsonify(error="Missing password"), 400

    user = UserModel.query.filter_by(email = user_email).first()
    if user:
        return jsonify(error="User with email already exists"), 400

    encrypted_password = hashlib.sha256(user_password.encode('utf-8')).hexdigest()

    user = UserModel(email=user_email, password=encrypted_password, role="basic")
    db.session.add(user)
    db.session.commit()
    return {
        'id': user.id
    }

@app.route("/users/<user_id>", methods = ['GET'])
@authenticate
@limiter.limit("10/minute")
def users_get(user, user_id):
    print(user_id)
    user = UserModel.query.get(user_id)
    if not user:
        return jsonify(error="User not found"), 404

    response = {
        'id': user.id,
        'email': user.email,
        'role': user.role,
    }
    return response

@app.after_request
def log_request_data(response):
    app.logger.debug('Response Headers: %s', response.headers)

    request_body = ''
    if request.path.startswith('/login'):
        request_body = 'REDACTED'
    elif request.get_data():
        request_body = str(request.get_data())

    response_body = str(response.get_json())
    if request.path.startswith('/login'):
        response_body = 'REDACTED'
        
    app.logger.debug('Response Body: %s', response_body)
            

    sanitized_headers = ''
    for key, val in request.headers:
        if key != 'X-Access-Token':
            sanitized_headers += f'{key}: {val}\n'

    logs = LogsModel(user_id=1, url=request.url, headers=str(sanitized_headers), request=request_body, response=response_body)
    db.session.add(logs)
    db.session.commit()

    return response

if __name__ == "__main__":
    app.run()