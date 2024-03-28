""""FastAPI yolo."""

import logging
import uuid
from collections.abc import Sequence
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import Session, SQLModel, create_engine, select

from pyphoria.models import Character, Inventory, InventoryItemLink, Item

SQLITE_DB = "database.db"
sqlite_url = f"sqlite:///{SQLITE_DB}"


log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)

def create_db_and_tables():  # noqa: ANN201, D103
    SQLModel.metadata.create_all(engine)



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/character/")
def create_character(character: Character) -> Character:
    with Session(engine) as session:
        session.add(character)
        session.commit()
        session.refresh(character)
        return character


@app.get("/character/")
def get_characters() -> Sequence[Character]:
    with Session(engine) as session:
        characters = session.exec(select(Character)).all()
        return characters

@app.get("/character/{character_id}")
def get_character(character_id: uuid.UUID) -> Character | None:
    with Session(engine) as session:
        character = session.get(Character, character_id)
        return character

@app.put("/character/{character_id}")
def update_character(character_id: uuid.UUID, character: Character) -> Character:
    with Session(engine) as session:
        character = session.get(Character, character_id)
        character.update(character)
        session.add(character)
        session.commit()
        session.refresh(character)
        return character


@app.get("/character/{character_id}/inventory")
def get_inventory(character_id: uuid.UUID) -> tuple[Inventory, list[Item] | None] | None:
    with Session(engine) as session:
        character = session.get(Character, character_id)
        if character is None:
            return None
        items_ids: Sequence[uuid.UUID] = session.exec(select(InventoryItemLink.item_id).where(InventoryItemLink.inventory_id == character.inventory_id)).all()
        inventory: Inventory | None =  session.get(Inventory, character.inventory_id)

        if not items_ids:
            return (inventory, None)

        items: list[Item] = []
        for item_id in items_ids:
            item = session.get(Item, item_id)
            items.append(item)
        return (inventory, items)


@app.get("/inventory/")
def get_inventories() -> Sequence[Inventory]:
    with Session(engine) as session:
        inventories = session.exec(select(Inventory)).all()
        return inventories

@app.get("/inventory/{inventory_id}")
def get_inventory(inventory_id: uuid.UUID) -> tuple[Inventory, list[Item] | None] | None:
    with Session(engine) as session:
        inventory = session.get(Inventory, inventory_id)
        item_ids = session.exec(select(InventoryItemLink.item_id).where(InventoryItemLink.inventory_id == inventory_id)).all()
        if not item_ids:
            return (inventory, None)
        items: list[Item] = []
        for item_id in item_ids:
            item: Item | None = session.get(Item, item_id)
            items.append(item)
        return (inventory, items)
