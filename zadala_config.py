import os

database = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": os.environ["DB_NAME"] if "DB_NAME" in os.environ else "zadala",
    "USER": os.environ["DB_USER"] if "DB_USER" in os.environ else "postgres",
    "PASSWORD": os.environ["DB_PASS"] if "DB_PASS" in os.environ else "1",
    "HOST": os.environ["DB_HOST"] if "DB_HOST" in os.environ else "localhost",
    "PORT": os.environ["DB_PORT"] if "DB_PORT" in os.environ else "5432",
}
