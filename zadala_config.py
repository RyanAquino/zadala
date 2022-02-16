database = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": "zadala",
    "USER": "postgres",
    "PASSWORD": "1",
    "HOST": "localhost",
    "PORT": "5432",
}

redis_database = {
    "REDIS_URL": "redis://localhost:6379/0",
}

ZADALA_SECRET_KEY = "my-secret"

EMAIL_HOST_PROVIDER = "smtp.gmail.com"
EMAIL_HOST_PORT = 587
EMAIL_HOST_USER = "gmail email"
EMAIL_HOST_PASSWORD = "gmail password"

GOOGLE_CLIENT_ID = "Google client ID"
GOOGLE_CLIENT_SECRET = "Google client secret"
