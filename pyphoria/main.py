""""FastAPI yolo."""

import logging
import uuid
from collections.abc import Sequence
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import ResponseValidationError
from pydantic import PositiveInt
from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine, select

from pyphoria.models import (
    Character,
    CharacterCreate,
    CharacterRead,
    HTTPError,
    Inventory,
    InventoryItemLink,
    Item,
    Species,
    SpeciesRead,
)

SQLITE_DB = "database.db"
sqlite_url = f"sqlite:///{SQLITE_DB}"


log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

connect_args = {"check_same_thread": False}
engine: Engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)


def create_db_and_tables():  # noqa: ANN201, D103
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/species/")
async def get_species() -> Sequence[SpeciesRead]:
    with Session(engine) as session:
        species = session.exec(select(Species)).all()
        return species


@app.get("/character/", response_model=list[CharacterRead])
async def get_characters() -> Sequence[CharacterRead]:
    with Session(engine) as session:
        characters = session.exec(select(Character)).all()
        return characters


@app.post("/character/", response_model=CharacterRead)
async def create_character(character: CharacterCreate) -> CharacterCreate:
    with Session(engine) as session:
        db_character: CharacterCreate = CharacterCreate.model_validate(character)
        session.add(db_character)
        session.commit()
        session.refresh(db_character)
        return db_character


@app.get("/character/{character_id}")
async def get_character(character_id: uuid.UUID) -> CharacterRead:
    with Session(engine) as session:
        try:
            character = session.get(Character, character_id)
            return character
        except ResponseValidationError:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Character not found",
            )
        if not character:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Character not found",
            )


@app.put("/character/{character_id}")
async def update_character(
    character_id: uuid.UUID,
    character: CharacterRead,
) -> Character:
    with Session(engine) as session:
        character = session.get(Character, character_id)
        character.update(character)
        session.add(character)
        session.commit()
        session.refresh(character)
        return character


@app.get(
    "/character/{character_id}/inventory",
    responses={
        # 200: {"model": Dummy},
        404: {
            "model": HTTPError,
            "description": "Character not found",
        },
    },
)
async def get_character_inventory(
    character_id: uuid.UUID,
) -> Inventory | None:
    with Session(engine) as session:
        character = session.get(Character, character_id)
        if not character:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail="Character not found",
            )
        return session.get(Inventory, character.inventory_id)


@app.get("/inventory/")
async def get_inventories() -> Sequence[Inventory]:
    with Session(engine) as session:
        inventories = session.exec(select(Inventory)).all()
        return inventories


@app.get("/inventory/{inventory_id}")
async def get_inventory(
    inventory_id: uuid.UUID,
) -> Inventory | None:
    with Session(engine) as session:
        return session.get(Inventory, inventory_id)


@app.post("/inventory/")
async def create_inventory(inventory: Inventory) -> Inventory:
    with Session(engine) as session:
        session.add(inventory)
        session.commit()
        session.refresh(inventory)
        return inventory


@app.put("/inventory/{inventory_id}")
async def update_inventory(inventory_id: uuid.UUID, inventory: Inventory) -> Inventory:
    with Session(engine) as session:
        inventory = session.get(Inventory, inventory_id)
        inventory.update(inventory)
        session.add(inventory)
        session.commit()
        session.refresh(inventory)
        return inventory


@app.delete("/inventory/{inventory_id}")
async def delete_inventory(inventory_id: uuid.UUID) -> Inventory | None:
    with Session(engine) as session:
        inventory: Inventory | None = session.get(Inventory, inventory_id)
        if not inventory:
            return None
        character: Character | None = session.exec(
            select(Character).where(Character.inventory_id == inventory_id),
        ).one_or_none()
        if character:
            character.inventory_id = None
            session.add(character)
            session.commit()
        session.delete(inventory)
        session.commit()
        return inventory


@app.post("/item/")
async def create_item(item: Item) -> Item:
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item


@app.get("/item/")
async def get_items() -> Sequence[Item]:
    with Session(engine) as session:
        items: Sequence[Item] = session.exec(select(Item)).all()
        return items


@app.get("/item/{item_id}")
async def get_item(item_id: uuid.UUID) -> Item | None:
    with Session(engine) as session:
        item: Item | None = session.get(Item, item_id)
        return item


@app.put("/item/{item_id}")
async def update_item(item_id: uuid.UUID, item: Item) -> Item:
    with Session(engine) as session:
        item = session.get(Item, item_id)
        item.update(item)
        session.add(item)
        session.commit()
        session.refresh(item)
        return item


@app.delete("/item/{item_id}")
async def delete_item(item_id: uuid.UUID) -> Item:
    with Session(engine) as session:
        item: Item | None = session.get(Item, item_id)
        if not item:
            log.info("Item %s not found", item_id)
            return None
        inventories_with_item: Sequence[InventoryItemLink] = session.exec(
            select(InventoryItemLink).where(InventoryItemLink.item_id == item_id),
        ).all()
        for inventory in inventories_with_item:
            log.info(
                "Removing item %s from inventory %s",
                item_id,
                inventory.inventory_id,
            )
            _inventory: Inventory | None = session.get(
                Inventory,
                inventory.inventory_id,
            )
            if _inventory:
                _inventory.items.remove(item_id)
                session.add(_inventory)

        log.info("Deleting item %s", item_id)
        session.delete(item)
        session.commit()
        return item


@app.post("/inventory/{inventory_id}/item/{item_id}/{item_count}")
async def add_item_to_inventory(
    inventory_id: uuid.UUID,
    item_id: uuid.UUID,
    item_count: PositiveInt,
) -> Inventory:
    with Session(engine) as session:
        inventory: Inventory | None = session.get(Inventory, inventory_id)
        if not inventory:
            return ValueError(f"Inventory with id {inventory_id} not found")
        item: Item | None = session.get(Item, item_id)
        if not item:
            return ValueError(f"Item with id {item_id} not found")
        if item_id in inventory.items:
            return ValueError(f"Item with id {item_id} already in inventory")
        inventory.items.append(item_id)
        session.add(inventory)
        inventory_item_link = InventoryItemLink(
            inventory_id=inventory_id,
            item_id=item_id,
            item_count=item_count,
        )
        session.add(inventory_item_link)
        session.commit()
        return inventory
