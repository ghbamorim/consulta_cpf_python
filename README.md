# shipin app server

Shipin shore ais is an internal API for data processing for marine automatic identification system.

## Development environment


### Swagger

```bash
http://localhost:3000/api/v1/_docs#/
```

### Create a virtual environment

```bash
pip install virtualenv
```

```bash
python3 -m venv venv
```
or

```bash
python -m venv venv
```


Activating the virtual environment


```bash
. venv/Scripts/activate
```

Disabling the virtual environment

```bash
deactivate
```

### Installation of dependencies

In the main (shipin) project directory

```
shipin/
   deploy/
   helm/
   shipin-app-client/
   shipin-app-server/
   shipin-common/
   shipin-edge/
   shipin-shore-activity/
   shipin-shore-ais/
```

Run commands

```bash
pip install -e shipin-common
pip install -e shipin-shore-ais
pip install -e shipin-app-server
```

requirements.txt

```bash
Flask==2.0.1
psycopg2-binary==2.8.6
Flask-SQLAlchemy==2.5.1
Flask-JWT-Extended==4.2.3
Flask-Cors==3.0.10
stringcase==1.2.0
Flask-Admin==1.5.8
Flask-Migrate==3.0.1
graphene-sqlalchemy==2.3.0
graphene-sqlalchemy-filter==1.12.2
Flask-BasicAuth==0.2.0
gunicorn==20.0.4
SQLAlchemy==1.4.20
fsspec==0.8.7
s3fs==0.5.2
Flask-Mail==0.9.1
requests==2.25.1
var_dump==1.2
flasgger==0.9.5
faker
marshmallow==3.12.1
more_itertools==8.8.0
```

```bash
pip install -r requirements.txt
```

### Database

Create a dedicated postgres db (db_shipin_app_server) for the shipin-app-server


### Environment variable

Unix and MacOS

```bash
export DATABASE_URL=postgresql://postgres:123456@127.0.0.1:5435/db_shipin_app_server
export "FLASK_APP=shipin_app_server.app:create_app()"
export FLASK_ENV=development
export FLASK_DEBUG=1
```

Microsoft Windows

```bash
set DATABASE_URL=postgresql://postgres:123456@127.0.0.1:5435/db_shipin_app_server
set FLASK_APP=shipin_app_server.app:create_app()
set FLASK_ENV=development
set FLASK_DEBUG=1
```


## Usage

Run command to start app

```bash
flask run --host=0.0.0.0 --port=3000
```

## Migrations

In shipin/shipin-app-server/


Run the command to update or revert migrations

```bash
flask db upgrade

or

flask db downgrade
```

Run the command to create a new migrate

```bash
flask db migrate -m "Initial migration."
```


## Seeds

Set environment variable before run command:


Drop data base

```bash
shipin-app-server drop_db
```

Recreate data base

```bash
shipin-app-server reset_db
```

Create new user role

Ex: role = "Superuser" or "Admin" or "Viewer"

```bash
shipin-app-server create_user username password email role
```

Update password user

```bash
shipin-app-server update_password username new_password
```

Create users tests

Ex: count = 10

```bash
shipin-app-server create_users_test count
```

Generate data for tests

Ex: list_years = 2020,2021  (separated with commas)

```bash
shipin-app-server init_seed_db username new_password list_years
```


