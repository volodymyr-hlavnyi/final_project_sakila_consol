import dotenv
import os


def get_db_config():
    dotenv.load_dotenv()
    ICH_HOST = os.getenv("ICH_HOST")
    ICH_PASSWORD = os.getenv("ICH_PASSWORD")
    ICH_USER = os.getenv("ICH_USER")
    ICH_DATABASE = os.getenv("ICH_DATABASE")

    ICH_HOST_WRITE = os.getenv("ICH_HOST_WRITE")
    ICH_PASSWORD_WRITE = os.getenv("ICH_PASSWORD_WRITE")
    ICH_USER_WRITE = os.getenv("ICH_USER_WRITE")
    ICH_DATABASE_WRITE = os.getenv("ICH_DATABASE_WRITE")

    dbconfig = {
        "host": f"{ICH_HOST}",
        "user": f"{ICH_USER}",
        "password": f"{ICH_PASSWORD}",
        "database": f"{ICH_DATABASE}",
    }

    dbconfig_write = {
        "host": f"{ICH_HOST_WRITE}",
        "user": f"{ICH_USER_WRITE}",
        "password": f"{ICH_PASSWORD_WRITE}",
        "database": f"{ICH_DATABASE_WRITE}",
    }
    return dbconfig, dbconfig_write
