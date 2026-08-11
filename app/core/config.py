from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    DB_USER = os.getenv("POSTGRES_USER")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    DB_NAME = os.getenv("POSTGRES_DB")
    DB_PORT = os.getenv("POSTGRES_PORT")


settings = Settings()