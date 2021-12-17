from datetime import datetime

from Models import User, SolarPanelModel, SolarPanel, DataEntry, Base
import databaseConnection


def add_users(session):
    oribe = User(
        name="Oribe",
        email="morobengoa@solaris.net",
        password="mutriku123",
        username="oribe",
        first_surname="Oribe",
        second_surname="Oribe",
        enabled=True,
        role_id=1,
    )

    gorka = User(
        name="Gorka",
        email="gorggystm@solaris.net",
        password="mutriku123",
        username="gorggystm",
        first_surname="Gorka",
        second_surname="Gorka",
        enabled=True,
        role_id=1,
    )

    urko = User(
        name="Urko",
        email="rkolay@solaris.net",
        password="mutriku123",
        username="urko",
        first_surname="Urko",
        second_surname="Urko",
        enabled=True,
        role_id=1,
    )

    domaika = User(
        name="Domaika",
        email="aritz1019@solaris.net",
        password="mutriku123",
        username="domaika",
        first_surname="Domaika",
        second_surname="Domaika",
        enabled=True,
        role_id=1,
    )

    ekaitz = User(
        name="Ekaitz",
        email="eka95@solaris.net",
        password="mutriku123",
        username="ekaitz",
        first_surname="Ekaitz",
        second_surname="Ekaitz",
        enabled=True,
        role_id=1,
    )

    session.add(oribe)
    session.add(gorka)
    session.add(urko)
    session.add(domaika)
    session.add(ekaitz)


def add_panel_models(session):
    model1 = SolarPanelModel(
        code="OG_SOLAR_PANEL_MODEL_1",
        i18n="solar.models.ogSolarPanel1",
        power=355,
        price=249,
        width=1200,
        height=1800,
    )

    model2 = SolarPanelModel(
        code="OG_SOLAR_PANEL_MODEL_2",
        i18n="solar.models.ogSolarPanel2",
        power=450,
        price=350,
        width=1500,
        height=1800,
    )

    model3 = SolarPanelModel(
        code="SMALL_SOLAR_PANEL_MODEL_1",
        i18n="solar.models.smallSolarPanel1",
        power=150,
        price=179,
        width=800,
        height=1200,
    )

    model4 = SolarPanelModel(
        code="SMALL_SOLAR_PANEL_MODEL_2",
        i18n="solar.models.smallSolarPanel2",
        power=120,
        price=149,
        width=650,
        height=1000,
    )

    session.add(model1)
    session.add(model2)
    session.add(model3)
    session.add(model4)


def add_solar_panels(session):
    panel1 = SolarPanel(
        installed_on=datetime.now(),
        model_id=1,
        user_id=1,
    )

    panel2 = SolarPanel(
        installed_on=datetime.now(),
        model_id=1,
        user_id=3,
    )

    panel3 = SolarPanel(
        installed_on=datetime.now(),
        model_id=3,
        user_id=3,
    )

    panel4 = SolarPanel(
        installed_on=datetime.now(),
        model_id=4,
        user_id=3,
    )

    session.add(panel1)
    session.add(panel2)
    session.add(panel3)
    session.add(panel4)


if __name__ == "__main__":
    engine = databaseConnection.get_engine()
    Base.metadata.create_all(engine)
    session = databaseConnection.get_session()
    add_users(session)
    session.commit()
    add_panel_models(session)
    session.commit()
    add_solar_panels(session)
    session.commit()
