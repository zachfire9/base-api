# Base API

## Initialize DB

docker-compose up -d

## Start App

pip install virtualenv
virtualenv venv
source venv/bin/activate (venv\Scripts\activate)
$env:SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:admin@127.0.0.1:3306/base"
python main.py

## Features

* Rate Limiting
* Request/Response Logging

## ToDo

* Authentication
* ACL
* Swagger