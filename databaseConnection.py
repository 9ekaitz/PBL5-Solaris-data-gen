from json import loads

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

try:
    with open("db_config.json", "r", encoding="UTF-8") as f:
        db_config = loads(f.read())
except FileNotFoundError():
    print(
        "[ERROR] No se encontró el archivo de configuración de la base de datos. Asegurate de meterlo en la carpeta"
    )
    exit(1)

CONFIG = db_config["DB_CONFIG"]


def get_engine():
    driver = CONFIG["driver"]
    user = CONFIG["user"]
    password = CONFIG["password"]
    host = CONFIG["host"]
    port = CONFIG["port"]
    database = CONFIG["database"]

    engine_url = f"{driver}://{user}:{password}@{host}:{port}/{database}"

    return create_engine(engine_url)


def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()
