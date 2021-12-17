from datetime import datetime, timedelta
import traceback

from perlin_noise import PerlinNoise
from matplotlib import pyplot as plt

from Models import (
    SolarPanelModel,
    SolarHourProvincias,
    RelacionComunidadProvincia,
    SolarPanel,
    WeatherComunidad,
    DataEntry,
    Base,
)
import databaseConnection


NOISE_CONSTANT = 12
NOISE_BELOW_ZERO_FACTOR = 0.03
NOISE_NORMAL_FACTOR = 0.3
MINUTES = 60 * 24


def curve(x, hoffset, voffset, m):
    return -(((x - float(hoffset)) / m) ** 2) + float(voffset)


def apply_noise(y, x, noise_func, power):
    if y < 0:
        return (
            noise_func((x / MINUTES) * NOISE_CONSTANT)
            * float(power)
            * NOISE_BELOW_ZERO_FACTOR
        )
    else:
        return (
            noise_func((x / MINUTES) * NOISE_CONSTANT)
            * float(power)
            * NOISE_NORMAL_FACTOR
            + y
        )


def get_curve_properties(session, capital_provincia, month):
    solar_info = (
        session.query(SolarHourProvincias)
        .filter(SolarHourProvincias.capital_provincia == capital_provincia)
        .filter(SolarHourProvincias.mes == int(month))
        .first()
    )

    amanecer, anochecer, punto_algido = (
        solar_info.amanecer,
        solar_info.anochecer,
        solar_info.punto_algido,
    )

    rate = anochecer / amanecer * 10
    return punto_algido, rate


def get_panel_properties(session, panel_id):
    panel = session.query(SolarPanel).filter(SolarPanel.id == panel_id).first()
    model = (
        session.query(SolarPanelModel)
        .filter(SolarPanelModel.id == panel.model_id)
        .first()
    )
    rel = (
        session.query(RelacionComunidadProvincia)
        .filter(RelacionComunidadProvincia.id_provincia == panel.provincia_id)
        .first()
    )
    voltage = model.voltage
    power = model.power
    capital_provincia = rel.capital_provincia
    id_comunidad = rel.id_comunidad

    return capital_provincia, power, id_comunidad, voltage


def get_weather_factor(session, dt, id_comunidad):
    weather = (
        session.query(WeatherComunidad)
        .filter(WeatherComunidad.id_comunidad == id_comunidad)
        .filter(WeatherComunidad.timestamp_inicio >= dt)
        .filter(WeatherComunidad.timestamp_fin <= dt)
        .first()
    )
    return weather.tiempo


def data_point(x: datetime, power, highest_point, rate, weather_factor, noise_func):
    minute = x.hour * 60 + x.minute

    curve_point = curve(minute, highest_point, power, rate)
    # print("Curve point:", curve_point)
    noise_applied = apply_noise(curve_point, minute, noise_func, power)
    # print("Noise applied:", noise_applied)
    weather_applied = noise_applied * float(weather_factor)
    # print("Weather applied:", weather_applied)

    return weather_applied if weather_applied > 0 else 0


def generate_data(panel_id, dt_start, dt_end):
    try:
        noise_func = PerlinNoise(octaves=4, seed=dt_start.timestamp())
        session = databaseConnection.get_session()
        capital_provincia, power, id_comunidad, voltage = get_panel_properties(
            session, panel_id
        )

        current_dt = dt_start

        old_hour = None
        old_month = None

        x = []
        y = []

        while current_dt < dt_end:
            if old_month != current_dt.month:
                highest_point, rate = get_curve_properties(
                    session, capital_provincia, current_dt.month
                )
            if old_hour != current_dt.hour:
                weather_factor = get_weather_factor(session, current_dt, id_comunidad)
                old_hour = current_dt.hour

            generated = data_point(
                current_dt, power, highest_point, rate, weather_factor, noise_func
            )
            current_dt = current_dt + timedelta(minutes=1)
            x.append(current_dt)
            y.append(generated)
            entry = DataEntry(
                timestamp=current_dt,
                power=generated,
                voltage=voltage,
                current=generated / float(voltage),
                solar_panel_id=panel_id,
            )

        plt.plot(x, y)
        plt.show()

    except Exception as e:
        traceback.print_exc()
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    Base.metadata.create_all(databaseConnection.get_engine())
    generate_data(5, datetime(2019, 1, 1, 1, 0, 0), datetime(2019, 1, 10, 23, 59, 59))
