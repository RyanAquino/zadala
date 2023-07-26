# Zadala API
Zadala API is an ecommerce web API built with django rest framework.

### Endpoints
- `GET /admin` - Admin page
- `GET /api-docs` - Swagger API documentation 

### Requirements
- python 3
- docker
- docker-compose

### Technology
- Python 3
- Pytest
- Django rest framework
- PostgreSQL
- Redis
- AWS
- OAuth2
- NGINX


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
##### Creating Admin Super User
```
python manage.py createsuperuser
```
##### Run server
```
python manage.py runserver
```

##### Running RQ workers
```
python manage.py rqworker high default low
```

#### Access on browser
```
http://localhost:8000/api-docs
```

### Setup with Docker (Alternative)
```
docker-compose -f deployments/docker-compose.yml up -d
```

### Load initial data (Optional)
```
python manage.py loaddata resources/init_data.json
```

### Running tests with coverage
```
pytest . -v --cov
```