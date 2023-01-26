# Base API

## Features

* Rate Limiting
* Request/Response Logging
* JWT Authentication
* Swagger Docs

## Swagger Docs

Once the app is started you can replace the url with where the app is running on localhost:

```
{url}/api/docs
```

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

## ToDo

* ACL