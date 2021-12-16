from json import loads
from os.path import exists, join
from os import makedirs, listdir
from datetime import time
from re import split
from sys import exit

from requests import get, HTTPError
from sqlalchemy import create_engine
from pandas import DataFrame

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

LISTA_CIUDADES = json["LISTA_CIUDADES"]
URL_API = json["URL_API"]
DOWNLOAD_FOLDER = json["DOWNLOAD_FOLDER"]
DB_CONFIG = db_config["DB_CONFIG"]


def descargar_datos_txt(ciudad):
    url = URL_API.format(ciudad=ciudad)
    response = get(url)
    if response.status_code != 200:
        raise HTTPError(response.status_code)
    dest = DOWNLOAD_FOLDER + ciudad + ".txt"
    with open(dest, "w+") as f:
        f.write(response.text)


def descargar_todas_comunidades():
    if not exists(DOWNLOAD_FOLDER):
        makedirs(DOWNLOAD_FOLDER)

    for ciudad in LISTA_CIUDADES:
        if exists(join(DOWNLOAD_FOLDER, ciudad + ".txt")):
            continue
        try:
            descargar_datos_txt(ciudad)
            print("[INFO] Descargados datos de la ciudad:", ciudad)
        except HTTPError:
            print("[ERROR] Error descargando datos de la ciudad:", ciudad)


def get_engine(cfg):
    driver = cfg["driver"]
    user = cfg["user"]
    password = cfg["password"]
    host = cfg["host"]
    port = cfg["port"]
    database = cfg["database"]

    engine_url = f"{driver}://{user}:{password}@{host}:{port}/{database}"

    return create_engine(engine_url)


def map_s(datastr):
    hstr = datastr[-2:]
    mstr = datastr[:-2]
    t = time(int(mstr), int(hstr), 0)
    return t.hour * 60 + t.minute


def map_df(s):
    return s.apply(map_s).astype(int)


def process_months(mean):
    d = {}
    month_df = DataFrame()
    for index, item in mean.iteritems():
        mes = int(index / 2) + 1
        if index % 2 == 1:
            d = {"mes": mes, "salida": int(item)}
        else:
            d["puesta"] = int(item)
            month_df = month_df.append(d, ignore_index=True)
    return month_df


def get_df_ciudad(ciudad, lines):
    datalines = lines[7:35]
    datalines = [line.strip() for line in datalines]
    datalines = [
        split(
            "\s+",
            line,
        )
        for line in datalines
    ]
    df = DataFrame(datalines).drop(columns=0)
    df = df.apply(map_df)
    df = df.astype(int)
    mean = df.mean()
    months = process_months(mean).astype(int)
    months["capital_provincia"] = ciudad
    months["punto_algido"] = months.apply(
        lambda row: row["salida"] + (row["puesta"] - row["salida"]) / 2, axis=1
    ).astype(int)
    return months[
        ["capital_provincia", "mes", "salida", "puesta", "punto_algido"]
    ].rename({"salida": "amanecer", "puesta": "anochecer"}, axis=1)


def process_db_df():
    df = DataFrame()
    for file in listdir(DOWNLOAD_FOLDER):
        if file.endswith(".txt"):
            ciudad = file.split(".")[0].lower()
            with open(join(DOWNLOAD_FOLDER, file), "r") as f:
                lines = f.readlines()
            df_ciudad = get_df_ciudad(ciudad, lines)
            df = df.append(df_ciudad, ignore_index=True)
            print("[INFO] Procesados datos de la ciudad:", ciudad)
    return df


if __name__ == "__main__":
    descargar_todas_comunidades()
    db_df = process_db_df()
    engine = get_engine(DB_CONFIG)
    db_df.to_sql("solar_hours_provincias", engine, if_exists="replace", index=False)
    print("[SUCCESS] Datos subidos a la base de datos")
