import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(".")
ENV_DIR = BASE_DIR / ".env"


load_dotenv(ENV_DIR)
Config = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'db_url': f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
    'engine': 'django.db.backends.postgresql',

}
