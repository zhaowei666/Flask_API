1. Setup virtual enviroment
- $ virtualenv env
- $ source env/bin/activate
- $ pip install -r requirements.txt

2. Setup PostgreSQL database
- CREATE DATABASE player_db;
- CREATE USER dev_user WITH PASSWORD 'dev_password';
- GRANT ALL PRIVILEGES ON DATABASE "dev_db" to dev_user;


