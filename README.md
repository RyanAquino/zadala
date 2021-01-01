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
##### Edit `zadala_config.py` base on your needs
```
vi zadala_config.py
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
```
GET /admin - admin page
```
##### Run server
```
python manage.py runserver
```

### Setup with Docker (Alternative)
```
docker-compose up -d
```

### Load initial data (Optional)
```
python manage.py loaddata init_data.json
```

### Running tests
```
pytest .
```