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


class SolarPanel(Base):
    __tablename__ = "solar_panel"
    id = Column(Integer, primary_key=True)
    installed_on = Column(DateTime, nullable=False)
    model_id = Column(Integer, ForeignKey("solar_panel_model.id"))
    user_id = Column(Integer, ForeignKey("user.id"))


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
