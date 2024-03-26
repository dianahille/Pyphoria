import uuid
from typing import TYPE_CHECKING, List, Optional

from pydantic import (
    ConfigDict,
    PositiveInt,
)
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from pyphoria.models.Item import Item


class StrictBaseModel(SQLModel):  # noqa: D101
    class Config(ConfigDict):  # noqa: D106
        strict = True


class CharacterStats(SQLModel, table=False):  # noqa: D101
    stat_combat: PositiveInt
    stat_dodge_rating: PositiveInt
    stat_hit_rating: PositiveInt
    stat_intelligence: PositiveInt
    stat_luck: PositiveInt
    stat_vitality: PositiveInt


class Species(CharacterStats, table=True):  # noqa: D101
    id: uuid.UUID = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True,
        nullable=False,
    )
    name: str = Field(default=None, unique=True, index=True)
    description: str = Field(default=None)
    icon: str
    base_strength: PositiveInt
    base_dexterity: PositiveInt
    base_intelligence: PositiveInt


class Character(CharacterStats, table=True):  # noqa: D101
    # id: Uuid = Field(default_factory=uuid.uuid4, primary_key=True, unique=True)
    id: uuid.UUID = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True,
        nullable=False,
    )
    # account_id: uuid.UUID = Field(default=None, foreign_key="accounts.id")  # noqa: ERA001
    species: uuid.UUID = Field(foreign_key="species.id")
    name: str = Field(max_length=50, unique=True, index=True)
    surname: str
    level: PositiveInt = 1
    experience: PositiveInt = 0
    energy: PositiveInt
    inventory_id: uuid.UUID = Field(foreign_key="inventory.id")
    # inventory: Inventory | None = Relationship(back_populates="character_id")
    strength: PositiveInt
    dexterity: PositiveInt
    intelligence: PositiveInt


class InventoryExtension(SQLModel, table=True):  # noqa: D101
    id: uuid.UUID = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, unique=True,
    )
    slots: PositiveInt
    name: str = Field(max_length=50, unique=True, index=True)
    description: str
    icon: str


class Inventory(SQLModel, table=True):  # noqa: D101
    id: uuid.UUID = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, unique=True,
    )
    slots: PositiveInt
    gold: PositiveInt
    items: List["Item"] = Relationship(back_populates="inventory")
    # items: List["Item"]# = Relationship()
    #    back_populates="inventory", link_model=InventoryItemLink,
    # )
    # extensions: List["InventoryExtension"] = Relationship(
    #    back_populates="inventory",
    #    link_model=InventoryExtensionLink,
    # )


class ItemDamage(SQLModel, table=False):  # noqa: D101
    damage_fire: PositiveInt
    damage_physical: PositiveInt


class ItemRequirements(SQLModel, table=False):  # noqa: D101
    requirement_dexterity: PositiveInt
    requirement_intelligence: PositiveInt
    requirement_level: PositiveInt
    requirement_strength: PositiveInt


class Item(SQLModel, ItemDamage, ItemRequirements, table=True):  # noqa: D101
    id: uuid.UUID = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str = Field(max_length=50, unique=True, index=True)
    type: str
    description: str
    stackable: bool
    max_stack: PositiveInt
    unique_store: bool
    unique_equipped: bool
    icon: str
    inventory_id: Optional[uuid.UUID] = Field( # noqa: UP007
        default=None, foreign_key="inventory.id",
    )
    inventory = Optional[Inventory] = Relationship( # noqa: UP007
        back_populates="items",
    )


class Monster(SQLModel, table=True):  # noqa: D101
    id: uuid.UUID = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, unique=True,
    )
    name: str = Field(max_length=50, unique=True, index=True)
    description: str
    level: PositiveInt
    base_damage: PositiveInt
    icon: str


class Planet(SQLModel, table=True):
    """Planet model."""  # noqa: D203

    id: uuid.UUID = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, unique=True,
    )
    name: str = Field(max_length=50, unique=True, index=True)
    description: str
    icon: str
