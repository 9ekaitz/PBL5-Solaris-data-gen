from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Numeric, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class SolarPanelModel(Base):
    __tablename__ = "solar_panel_model"
    id = Column(Integer, primary_key=True)
    code = Column(String(50), nullable=False)
    i18n = Column(String(50), nullable=False)
    power = Column(Numeric, nullable=False)
    price = Column(Numeric, nullable=False)
    width = Column(Numeric, nullable=False)
    height = Column(Numeric, nullable=False)
    voltage = Column(Numeric, nullable=False)

    def __repr__(self):
        return f"<SolarPanelModel(id={self.id}, code={self.code}, i18n={self.i18n}, power={self.power}, price={self.price}, width={self.width}, height={self.height}, voltage={self.voltage})>"


class SolarPanel(Base):
    __tablename__ = "solar_panel"
    id = Column(Integer, primary_key=True)
    installed_on = Column(DateTime, nullable=False)
    model_id = Column(Integer, ForeignKey("solar_panel_model.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    provincia_id = Column(Integer)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    first_surname = Column(String(50), nullable=False)
    second_surname = Column(String(50), nullable=False)
    enabled = Column(Boolean, nullable=False)
    role_id = Column(Integer, nullable=True)


class DataEntry(Base):
    __tablename__ = "data_entry"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    power = Column(Numeric, nullable=False)
    voltage = Column(Numeric, nullable=False)
    current = Column(Numeric, nullable=False)
    solar_panel_id = Column(Integer, ForeignKey("solar_panel.id"))

    def __repr__(self):
        return f"<DataEntry(id={self.id}, timestamp={self.timestamp}, power={self.power}, voltage={self.voltage}, current={self.current}, solar_panel_id={self.solar_panel_id})>"


class SolarHourProvincias(Base):
    __tablename__ = "solar_hours_provincias"
    capital_provincia = Column(String, primary_key=True)
    mes = Column(Integer, primary_key=True)
    amanecer = Column(Integer)
    anochecer = Column(Integer)
    punto_algido = Column(Integer)

    def __repr__(self):
        return f"<SolarHourProvincias(capital_provincia={self.capital_provincia}, mes={self.mes}, amanecer={self.amanecer}, anochecer={self.anochecer}, punto_algido={self.punto_algido})>"


class RelacionComunidadProvincia(Base):
    __tablename__ = "relacion_comunidad_provincia"
    id_provincia = Column(Integer, primary_key=True)
    capital_provincia = Column(String)
    id_comunidad = Column(Integer)


class WeatherComunidad(Base):
    __tablename__ = "weather_comunidad"
    id_comunidad = Column(Integer, primary_key=True)
    timestamp_inicio = Column(DateTime, primary_key=True)
    timestamp_fin = Column(DateTime)
    tiempo = Column(Numeric)
