# Web Server Practice - Backend

This is web application server practice by tyoon9781

- Frontend (not in here)

  - Infra : AWS S3
  - Frontend Application : Next.js

- Backend

  - Infra : AWS EC2
  - Backend Application : fastapi
  - Web Server : Nginx
  - Middleware : uvicorn, gunicorn

- Database

  - DBMS : Postgresql
  - ORM : SQLAlchemy
  - Migration tool : alembic

# Environment Setting in EC2 Ubuntu OS

## AWS Settings

1. sg settings

```bash
## 3. AWS Security Group inbound edit.
 - ssh           / allowed_ip
 - http          / all ip
 - https         / all ip
 - postgresql    / allowed_ip
```

## Python

1. make python virtual environment
1. pip install

```bash
## 1. Python Virtual Environment
sudo apt update
sudo apt install -y python3.10-venv
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi python-dotenv alembic psycopg2-binary httpx uvicorn gunicorn
```

## Postgresql

1. install postgresql
1. access setting
1. make user, db

```bash
## 2.1 Postgresql Install
sudo apt install -y postgresql

## 2.2 Postgresql global Settings
allowed_ip={12.34.56.78}
psql_version={14}
echo "host all all ${allowed_ip}/32 scram-sha-256" | sudo tee -a /etc/postgresql/${psql_version}/main/pg_hba.conf
echo "listen_addresses = 'localhost,${allowed_ip}'" | sudo tee -a /etc/postgresql/${psql_version}/main/postgresql.conf
sudo service postgresql restart
sudo service postgresql status

## 2.3 Postgresql DB Create, User Create
cd /etc/postgresql
db_user_name={user}
db_user_password={password}
db_name="mydb"
test_db_name="testdb"
sudo -u postgres psql -c "CREATE USER ${db_user_name} WITH PASSWORD '${db_user_password}';"
sudo -u postgres psql -c "ALTER USER ${db_user_name} WITH SUPERUSER;"
sudo -u postgres psql -c "CREATE DATABASE ${db_name} WITH OWNER ${db_user_name};"
sudo -u postgres psql -c "CREATE DATABASE ${test_db_name} WITH OWNER ${db_user_name};"
```

## Nginx

remove default service, connect to gunicorn

```bash
sudo apt update
sudo apt install -y nginx
sudo mkdir /code
sudo nano nginx.conf
'''
server {
    listen {backend port};

    location / {
        proxy_pass http://unix:/tmp/gunicorn.sock;
    }
}
'''
sudo rm -rf /etc/nginx/sites-enabled/default
sudo service nginx restart
```

## Gunicorn

1. connect from nginx
1. uvicorn worker settings.
1. gunicorn systemd

```bash
## gunicorn configuration
cd /{project}/backend/
sudo nano gunicorn_config.py
'''
bind = "unix:/tmp/gunicorn.sock"
workers = 2
worker_class = "uvicorn.workers.UvicornWorker"
'''

## gunicorn service
sudo nano /etc/systemd/system/gunicorn.service
'''
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/practice/web_server/backend
ExecStart=/home/ubuntu/practice/web_server/backend/.venv/bin/gunicorn --config /home/ubuntu/practice/web_server/backend/gunicorn_config.py myapplication.app:app_instance
Restart=always

[Install]
WantedBy=multi-user.target
'''
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
```

## Git Hooks

.git/hooks/pre-commit file

```bash
#!/bin/bash

# Run pre_commit.py
python main_test.py

# Check the exit code of pre_commit.py
if [ $? -eq 0 ]; then
    echo "Tests passed. Continuing with the commit."

    # Update requirements.txt
    pip freeze > requirements.txt

    # Add requirements.txt to the staging area
    git add requirements.txt
else
    echo "Tests failed. Commit aborted."
    exit 1
fi
```
