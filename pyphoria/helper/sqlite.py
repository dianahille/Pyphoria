""""Interface!!!!!! to sqlite."""

import contextlib
import logging

import sqlalchemy
from sqlmodel import Session, SQLModel, create_engine, select

from pyphoria.models import Character, Inventory, Item, Monster, Planet, Species

SQLITE_DB = "database.db"
sqlite_url = f"sqlite:///{SQLITE_DB}"


log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

engine = create_engine(sqlite_url, echo=False)



def clear_db():  # noqa: ANN201, D103
    with Session(engine) as session, contextlib.suppress(
        sqlalchemy.exc.OperationalError,
    ):
        planets = session.exec(select(Planet))
        for planet in planets:
            session.delete(planet)

        monsters = session.exec(select(Monster))
        for monster in monsters:
            session.delete(monster)

        items = session.exec(select(Item))
        for item in items:
            session.delete(item)

        species = session.exec(select(Species))
        for specie in species:
            session.delete(specie)

        characters = session.exec(select(Character))
        for character in characters:
            session.delete(character)

        inventories = session.exec(select(Inventory))
        for inventory in inventories:
            session.delete(inventory)

        session.commit()


def create_db_and_tables():  # noqa: ANN201, D103
    SQLModel.metadata.create_all(engine)


def create_planets():  # noqa: ANN201, D103
    earth = Planet(
        name="Earth",
        description="The third planet from the Sun and the only astronomical object known to harbor life.",
        icon="earth.png",
    )
    with Session(engine) as session:
        session.add(earth)
        session.commit()


def create_stuff():

    session = Session(engine)

    # def create_monsters():
    goblin = Monster(
        name="Goblin",
        description="A small, grotesque, greedy, and evil creature that does evil things.",
        level=1,
        base_damage=1,
        icon="goblin.png",
    )
    session.add(goblin)
    session.commit()

    # def create_items():
    gun = Item(
        name="Gun",
        description="A weapon consisting of a metal tube, with mechanical attachments, from which projectiles are shot by the force of an explosive.",
        type="weapon",
        stackable=False,
        max_stack=1,
        unique_store=False,
        unique_equipped=False,
        requirement_level=1,
        requirement_strength=2,
        requirement_dexterity=1,
        requirement_intelligence=2,
        damage_fire=1,
        damage_physical=1,
        icon="gun.png",
    )
    sword = Item(
        name="Sword",
        description="A weapon consisting typically of a long, straight or slightly curved blade, sharp-edged on one or both sides, with one end pointed and the other fixed in a hilt or handle.",
        type="weapon",
        stackable=False,
        max_stack=1,
        unique_store=False,
        unique_equipped=False,
        requirement_level=1,
        requirement_strength=2,
        requirement_dexterity=1,
        requirement_intelligence=1,
        damage_fire=0,
        damage_physical=2,
        icon="sword.png",
    )
    session.add(gun)
    session.add(sword)
    session.commit()

    # def create_species():
    human = Species(
        name="Human",
        description="Yknow, humans.",
        icon="human.png",
        base_strength=1,
        base_dexterity=1,
        base_intelligence=1,
        stat_combat=1,
        stat_dodge_rating=1,
        stat_hit_rating=13,
        stat_intelligence=1,
        stat_luck=1,
        stat_vitality=1,
    )
    alien = Species(
        name="Alien",
        description="Yknow, aliens.",
        icon="alien.png",
        base_strength=1,
        base_dexterity=1,
        base_intelligence=1,
        stat_combat=1,
        stat_dodge_rating=1,
        stat_hit_rating=1,
        stat_intelligence=3,
        stat_luck=1,
        stat_vitality=1,
    )
    session.add(human)
    session.add(alien)
    session.commit()

    peter_inventory = Inventory(
        slots=10,
        gold=110,
    )
    jaqueline_inventory = Inventory(
        slots=10,
        gold=120,
    )

    peter = Character(
        species=human.id,
        name="Peter",
        surname="Parker",
        level=1,
        experience=0,
        energy=10,
        inventory_id=peter_inventory.id,
        strength=1,
        dexterity=1,
        intelligence=1,
        stat_combat=1,
        stat_dodge_rating=1,
        stat_hit_rating=13,
        stat_intelligence=1,
        stat_luck=1,
        stat_vitality=1,
    )
    jaqueline = Character(
        species=alien.id,
        name="Jaqueline",
        surname="Smith",
        level=1,
        experience=0,
        energy=10,
        inventory_id=jaqueline_inventory.id,
        strength=1,
        dexterity=1,
        intelligence=1,
        stat_combat=1,
        stat_dodge_rating=1,
        stat_hit_rating=13,
        stat_intelligence=1,
        stat_luck=1,
        stat_vitality=1,
    )
    session.add(peter_inventory)
    session.add(jaqueline_inventory)
    session.add(peter)
    session.add(jaqueline)
    peter_inventory.items.append(gun)
    jaqueline_inventory.items = [sword, gun]
    print("Jaqueline inventory items:")
    for _item in jaqueline_inventory.items:
        print("- " + _item.name)
    session.commit()


def main():  # noqa: ANN201, D103
    clear_db()
    create_db_and_tables()
    create_planets()
    create_stuff()
    # create_monsters()
    # create_items()
    # create_species()
    # create_characters()


if __name__ == "__main__":
    main()
