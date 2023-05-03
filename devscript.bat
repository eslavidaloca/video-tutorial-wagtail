@ECHO OFF

ECHO Running all migrations and running server

c:\
cd C:\Users\jonathan.medina\Documents\projects\wagtail_learning\newsite

python manage.py makemigrations
python manage.py migrate
python manage.py runserver
