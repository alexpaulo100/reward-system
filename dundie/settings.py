import os

SMTP_HOST = "localhost"
SMTP_PORT = 8025
SMTP_TIMEOUT = 5

DATEFMT: str = "%d/%m/%Y %H:%M:%S"
API_BASE_URL: str = (
    "https://economia.awesomeapi.com.br/json/last/USD-{currency}"
)

EMAIL_FROM = "master@dundie.com"
ROOT_PATH = os.path.dirname(__file__)
DATABASE_PATH = os.path.join(ROOT_PATH, "..", "assets", "database.db")
SQL_CON_STRING = f"sqlite:///{DATABASE_PATH}"

SALT_KEY = (
    "zx70WB2OhhzAMYD6VaDLZqpF3F77hOpDscExC8sIKx0RwZuok_KBg-L5RRyM4rN9VuU"
)
