""""Interface!!!!!! to sqlite."""


import contextlib

import sqlalchemy
from sqlmodel import Session, SQLModel, create_engine, select

from pyphoria.models.Monster import MonsterModel
from pyphoria.models.Planet import PlanetModel

SQLITE_DB = "database.db"
sqlite_url = f"sqlite:///{SQLITE_DB}"

engine = create_engine(sqlite_url, echo=True)

def clear_db():
    with Session(engine) as session, contextlib.suppress(sqlalchemy.exc.OperationalError):
        planets = session.exec(select(PlanetModel))
        for planet in planets:
            print(planet)
            session.delete(planet)
        session.commit()

        monsters = session.exec(select(MonsterModel))
        for monster in monsters:
            print(monster)
            session.delete(monster)
        session.commit()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_planets():
    earth = PlanetModel(name="Earth", description="The third planet from the Sun and the only astronomical object known to harbor life.", icon="earth.png")
    with Session(engine) as session:
        session.add(earth)
        session.commit()

def create_monsters():
    goblin = MonsterModel(name="Goblin", description="A small, grotesque, greedy, and evil creature that does evil things.", level=1, base_damage=1, icon="goblin.png")
    with Session(engine) as session:
        session.add(goblin)
        session.commit()


def main():
    clear_db()
    create_db_and_tables()
    create_planets()
    create_monsters()


if __name__ == "__main__":
    main()
