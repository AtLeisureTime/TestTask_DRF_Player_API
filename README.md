# TestTask_DRF_Player_API
## Tech stack
* Python 3.10
* Django 4.1
* djangorestframework
* django-filter
* SQLite

## Tech description
* Extra field on Django's many-to-many relationship
* Usage of django.db.models.constraints.UniqueConstraint
* Validation of unique constraints in rest framework serialisers (workaround of https://github.com/encode/django-rest-framework/issues/7173)
* REST API (GET, POST, PATCH, DELETE methods), Swagger UI

## Run locally
```
git clone https://github.com/AtLeisureTime/TestTask_DRF_Player_API.git
cd TestTask_DRF_Player_API/

python3 -m venv my_env
source my_env/bin/activate
pip install -r requirements.txt

cd app/
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
..
deactivate
```
