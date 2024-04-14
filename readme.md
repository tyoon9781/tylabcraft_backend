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

    # Check if requirements.txt has changed
    if ! git diff --quiet --exit-code -- requirements.txt; then
        echo "Updating requirements.txt"
        # Add requirements.txt to the staging area
        git add requirements.txt
    else
        echo "No changes in requirements.txt. Skipping commit."
    fi
else
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

## Alembic

reference : https://alembic.sqlalchemy.org/en/latest/tutorial.html

### init

```bash
alembic init alembic_db
alembic init alembic_testdb
```

### alembic_db.ini db_url settings

```bash
sqlalchemy.url = %(DB_URL)s
```

### alembic_testdb.ini db_url settings

```bash
sqlalchemy.url = %(TEST_DB_URL)s
```

### alembic_db/env.py, alembic_testdb/env.py

```python
from myapplication.database.model import Base
target_metadata = Base.metadata
```

### first Migration

```bash
## test db
alembic -c alembic_testdb.ini revision -m "init testdb"
alembic -c alembic_testdb.ini upgrade head
## db
alembic -c alembic_db.ini revision -m "init db"
alembic -c alembic_db.ini upgrade head
```

### change db, migration

```bash
## example Description
alembic -c alembic_testdb.ini revision --autogenerate -m "[title] [description]"
alembic -c alembic_testdb.ini upgrade head

alembic -c alembic_db.ini revision --autogenerate -m "[title] [description]"
alembic -c alembic_db.ini upgrade head
```

## how to make api?

### 1. Make Model (Example : User)

```python
## reference : https://fastapi.tiangolo.com/tutorial/sql-databases/
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, index=True, unique=True)
    username = Column(String, index=True, unique=True)
    password = Column(String)
    is_active = Column(Boolean)
```

### 2. Make Schema

```python
class UserSchema:
    class UserCreate(BaseModel):
        email: str
        username: str
        password: str

    class UserOut(BaseModel):
        username: str
        email: str
```

### 3. Make Crud

```python
class UserCrud:
    @classmethod
    def create_user(cls, user:UserSchema.UserCreate, db:Session) -> UserSchema.UserOut:
        ## password -> hash_password
        hash_password = get_hash_password(user.password)
        db_user = UserModel(**user.model_dump())

        db.add(db_user)
        db.commit()
        return db_user
```

### 4. Make API

```python
@router.post("/users", response_model=UserSchema.UserOut)
async def create_user(user:UserSchema.UserCreate, db:Session=Depends(conn_db.get_db)):
    return UserCrud.create_user(user, db)
```

### 5. Test

```python
class TestCaseV1(unitttest.TestCase):
    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_create_user(self):
        ...
```

## Attack -> Defense checklist

1. XSS -> sanitization
1. CSRF, SSRF -> csrf token, samesite cookie, CORS policy
1. SQL injection -> parameter query, ORM
1. DDoS -> WAF(Web Application Firewall), Traffic limit, IP block, CDN
1. Packet hijacking -> https
1. Cookie Poisoning -> Session managing
1. DB leak -> password Encryption, salt and pepper
1. System Broken -> Backup Container, Snapshot
