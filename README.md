# Zadala API
### Requirements
- python 3
- docker
- docker-compose

### Technology
- python 3
- pytest
- django rest framework
- PostgreSQL


### Setup
##### create virtual environment
```
python -m venv venv
```
##### Install required packages
```
pip install -r requirements.txt
```
##### Setup Postgres Database with Docker
```
docker-compose up && docker-compose rm -fsv
```

##### Migrate database
```
python manage.py migrate
```
##### Populate groups
```
python groups.py
```
##### Creating Admin Super User
```
python manage.py createsuperuser
```
##### Run server
```
python manage.py runserver
```

### Load initial data (Optional)
```
python manage.py loaddata init_data.json
```

### Running tests
```
pytest .
```