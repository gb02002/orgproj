# Installation guide
 
## This is the usual Django intallation guide.

1. Clone this repo:

	git clone https://github.com/yourusername/CharityNL.git

2. Install requirements(in case you are not sure what you are doing, create virtual environment(https://docs.python.org/3/library/venv.html)):

	cd CharityNl && pip install -r requirements.txt

3. Run migration: 
You should have a SQL-database configured. Project was make with Postgesql, but it should be compatable with most of others SQL-databases(for instance SQLlite).

	python manage.py migrate

4. Create missing configuration files. 

Most of git repos exlude sensitive settings files on behalf of security, so you would need to create them by youself. Here is the list of missing files:

	settings.py
	optional: gunicorn_config.py
	optional: celery.py

1. Fullfill variables. 

I use .env-files to avoid storing my passwords and other sensitive data in the project, so be aware, that you would need to generate a Django Secret Key and either pass it as Environment Varialbe(export VAR1=VAL1) or edit Settings.py manually. 

6. You are ready to take off:

	python manage.py runserver
