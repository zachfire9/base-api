import logging
import logging.config
import os
import yaml

from flask import Flask, request, abort, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from models import db, LogsModel, UserModel

app = Flask(__name__)
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
        if key != 'Authorization':
            sanitized_headers += f'{key}: {val}\n'

    app.logger.debug('Request Headers: %s', str(sanitized_headers))
    app.logger.debug('Request Body: %s', request.get_data())

@app.before_request
def authenticate():
    if not request.authorization.get('username'):
        return jsonify(error="Missing credentials"), 400

    email = request.authorization.get('username')
    user = UserModel.query.filter_by(email = email, role = 'admin').first()

    if not user:
        return jsonify(error="Invalid login"), 401

@app.route("/", methods = ['POST', 'GET'])
@limiter.limit("10/minute")
def index():
    return jsonify(error="Route not implemented"), 501

@app.route("/users", methods = ['POST'])
@limiter.limit("10/minute")
def users():
    user_email = request.get_json().get('email')
    if not user_email:
        return jsonify(error="Missing email"), 400

    user = UserModel.query.filter_by(email = user_email).first()
    if user:
        return jsonify(error="User with email already exists"), 400

    user = UserModel(email=user_email, role="basic")
    db.session.add(user)
    db.session.commit()
    return {
        'id': user.id
    }

@app.route("/users/<user_id>", methods = ['GET'])
@limiter.limit("10/minute")
def users_get(user_id):
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
    app.logger.debug('Response Body: %s', response.get_json())

    request_body = ''
    if request.get_data():
        request_body = str(request.get_data())

    sanitized_headers = ''
    for key, val in request.headers:
        if key != 'Authorization':
            sanitized_headers += f'{key}: {val}\n'

    logs = LogsModel(user_id=1, url=request.url, headers=str(sanitized_headers), request=request_body, response=str(response.get_json()))
    db.session.add(logs)
    db.session.commit()

    return response

if __name__ == "__main__":
    app.run()