from json import loads
from datetime import datetime, timedelta

from perlin_noise import PerlinNoise
from numpy.random import randint
from pandas import DataFrame
from sqlalchemy import create_engine


with open("datagen_config.json", "r", encoding="UTF-8") as f:
    json = loads(f.read())

try:
    with open("db_config.json", "r", encoding="UTF-8") as f:
        db_config = loads(f.read())
except FileNotFoundError():
    print(
        "[ERROR] No se encontró el archivo de configuración de la base de datos. Asegurate de meterlo en la carpeta"
    )
    exit(1)

DB_CONFIG = db_config["DB_CONFIG"]
COMUNIDADES = json["COMUNIDADES_AUTONOMAS"]


def get_engine(cfg):
    driver = cfg["driver"]
    user = cfg["user"]
    password = cfg["password"]
    host = cfg["host"]
    port = cfg["port"]
    database = cfg["database"]

    engine_url = f"{driver}://{user}:{password}@{host}:{port}/{database}"

    return create_engine(engine_url)


def lerp(a, b, t):
    return (1.0 - t) * a + b * t


def inv_lerp(a, b, v):
    return (v - a) / (b - a)


def remap(i_min, i_max, o_min, o_max, v):
    t = inv_lerp(i_min, i_max, v)
    return lerp(o_min, o_max, t)


def normalize_timestamp(dt):
    ts_start = datetime(2019, 1, 1, 0, 0, 0).timestamp()
    return dt.timestamp() - ts_start


def gen_weather_data(dt_start, dt_end):
    seed = randint(0, 100000)
    noise = PerlinNoise(octaves=4, seed=seed)
    x, y = [], []

    while dt_start < dt_end:
        ts = normalize_timestamp(dt_start)
        n = noise.noise(ts / 1000000)
        dt_start = dt_start + timedelta(hours=1)
        y.append(n)
        x.append(dt_start)

    return x, y


def generate_db_df(x, y, nombre_comunidad):
    df = DataFrame(
        {
            "nombre_comunidad": nombre_comunidad,
            "timestamp_inicio": x,
            "timestamp_fin": [x - timedelta(microseconds=1) for x in x],
            "tiempo": y,
        }
    )
    return df


def timeit(function):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = function(*args, **kwargs)
        end = datetime.now()
        print(f"{function.__name__} took {end - start} to complete.")
        return result

    return wrapper


@timeit
def main(dt_start, dt_end, nombre_comunidad, offset_comunidad):
    x, y = gen_weather_data(dt_start, dt_end)
    y = [remap(min(y), max(y), 0, 1, i) + offset_comunidad for i in y]

    df = generate_db_df(x, y, nombre_comunidad)
    engine = get_engine(DB_CONFIG)
    df.to_sql("weather_comunidad", engine, if_exists="append", index=False)


if __name__ == "__main__":
    dt1 = datetime(2019, 1, 1, 0, 0, 0)
    dt2 = datetime(2023, 12, 31, 23, 23, 0)

    for comunidad, offset in COMUNIDADES:
        print(comunidad)
        main(dt1, dt2, comunidad, offset)
