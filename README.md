# Base API

API template that can be used as a starting point for a new service

## Features

* Rate Limiting
* Request/Response Logging
* JWT Authentication
* Swagger Docs

## Initialize DB

```
docker-compose up -d
```

## Configure App Environment

### Install virtualenv

```
pip install virtualenv
```

### Create new virtual environment

```
virtualenv venv
```

### Start virtual environment

#### Mac/Linux 

```
source venv/bin/activate
```

#### Windows

```
venv\Scripts\activate
```

### Install Modules

Once you've started your virtual environment run:

```
pip install -r requirements.txt
```

## Start App

### Mac/Linux

Start virtual environment:

```
source venv/bin/activate
```

Set local environment variables every time you start your environment:

```
env $(cat .env | xargs)
```

Start the app:

```
python main.py
```

### Windows

Start virtual environment:

```
venv\Scripts\activate
```

Set local environment variables via PowersShell every time you start your environment:

```
.\bin\env.ps1
```

Start the app:

```
python main.py
```

## Unit Tests

Run the unit test from the root of the project:

```
python -m unittest tests\validate\test_user.py
```

## ToDo

Implement Flask-Authorize for ACL and RBAC:
https://flask-authorize.readthedocs.io/en/latest/