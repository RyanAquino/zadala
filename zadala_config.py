database = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": "zadala",
    "USER": "postgres",
    "PASSWORD": "1",
    "HOST": "localhost",
    "PORT": "5432",
}


REDIS_DATABASE = {
    "HOST": "redis",
    "PORT": 6379,
    "DB": 0,
    "PASSWORD": "",
}


ZADALA_SECRET_KEY = "my-secret"

EMAIL_HOST_PROVIDER = "smtp.gmail.com"
EMAIL_HOST_PORT = 587
EMAIL_HOST_USER = "gmail email"
EMAIL_HOST_PASSWORD = "gmail password"

GOOGLE_CLIENT_ID = "Google client ID"
GOOGLE_CLIENT_SECRET = "Google client secret"
AWS_SECRET_KEY_ID = "AWS secret key ID"
AWS_SECRET_ACCESS_KEY = "AWS secret access key"
AWS_SNS_ARN = "AWS SNS ARN"
