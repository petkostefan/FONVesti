# Intro

FONVesti is a website made in Django with a main goal of keeping university students up to date.
It allows students to register and pick their areas of interest allowing them to get notified via email withoud needing to refresh subject pages all day.

# How it works

Django runs the website, meanwhile Celery dispaches two tasks, both scraping news from university websites using requests and BeautifulSoup. If there are new posts, they are saved in the database and emails are sent to users interested in that area.

# Feautres

 - Scroll trough main news for undergraduate studies
 - Check latest news for different subjects and semesters (Only 4th semester is complete for demo)
 - Register and get notified when new posts are posted.
 - Use API to get news

# Tech
 - Frontend: Bootstrap
 - Backend: Django
 - Database: Sqlite3
 - Scraping: BeautifulSoup4
 - Task scheduler: Celery
 - Message broker: Redis
 - Infinite scroll: Waypoints.js

# Installation

Installation is done in few easy steps:
1. Cloning the repository and creating virtual enivronment
2. Installing requirements
3. Installing and running a message broker
4. Generating key and creating .env file
5. Setting up Google account and updating .env file
6. Migrate database
7. Create superuser
8. Populate database
9. Run commands

Clone the repository and create a virtual env:
```sh
git clone https://github.com/petkostefan/FONVesti.git
cd FONVesti
python -m venv venv
venv/Scripts/activate
```
Install requirements:
```python
pip install -r requirements.txt
```

Install and run a message broker (Redis, RabbitMQ, etc.). 
Here is a guide for installing Rabbitmq on Windows.
https://www.rabbitmq.com/install-windows.html#installer

After that we need to create .env file in folder fonvesti and write down our secret key, but before that we need to generate it.
```sh
py mange.py generatekey
```
In folder FONVesti/fonvesti create file named '.env'. It's content should look like this:
```
SECRET_KEY = %PASTE_YOUR_GENERATED_KEY_HERE%
````

Now, if you want to send mails (from google account), you will need to enable 2-Step Verification and App passwords.
It is pretty straihgt forward. Go to Manage your Google account > Security and enable these features. Don't forget to copy the 16 character password you get.
After copying the password update .env file:
```
SECRET_KEY = %YOUR_KEY_HERE%

EMAIL_HOST_USER = %YOUR_EMAIL_HERE%
EMAIL_HOST_PASSWORD = %YOUR_16CHAR_PASSWORD_HERE%
````
For example:
```
SECRET_KEY = -cm39v=xg&=2vnhb9e_e#wi@xx%^g)n_rea)prgagqdqr=24@h

EMAIL_HOST_USER = johndoe@gmail.com
EMAIL_HOST_PASSWORD = 16charpassword16
```


Migrate database:
```
py manage.py makemigrations
py manage.py migrate
```

Create superuser and fill username and password:
```
py manage.py createsuperuser
```

Next we need to prepare our database. We will use the following command:
```
py manage.py resetdatabase
```
This will delete all previous news and update every topic with 5 latest news.

Finally we can start everything up. Paste each command in a new terminal.
1. Run the server and open the website in browser:
```
py manage.py runserver
```
2. Run the beat (Task dispacher):
```
celery -A fonvesti beat -l INFO
```
3. Run the worker:
```
celery -A fonvesti worker -l INFO -P solo
```

# Testing
To test everything register a new account a check "Osnovne studije" (Undergraduate studies).

Simulate a new post by deleting the last one with the following command:
```
py manage.py deletelastpost
```
After a few secconds, you should recieve an email notification with a link to the new post.