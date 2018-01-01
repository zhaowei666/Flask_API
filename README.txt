1. Clone repo from github
- $ git clone https://github.com/zhaowei666/NFL_players.git
- $ cd NFL_players

2. Setup virtual enviroment
- $ virtualenv env
- $ source env/bin/activate
- $ pip install -r requirements.txt

3. Setup PostgreSQL database
- Download and open PostgreSQL. Follow instructions on https://www.postgresql.org/download/
- Set Port 5430
- $ CREATE DATABASE player_db;
- $ CREATE USER dev_user WITH PASSWORD 'dev_password';
- $ GRANT ALL PRIVILEGES ON DATABASE "dev_db" to dev_user;

4. Upgrade database and insert data
- $ python manage.py db migrate --message 'First migration'
- $ python manage.py db upgrade
- $ python add_data.py

5. Run application
- python manage.py run
- Open browser and go to http://player.lvh.me:5000/
- Select player and click 'Submit' button

For more information or help, email rzwdsg@gmail.com