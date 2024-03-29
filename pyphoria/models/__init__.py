import uuid
from typing import TYPE_CHECKING

from pydantic import (
    BaseModel,
    ConfigDict,
    NonNegativeInt,
    PositiveInt,
)
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from pyphoria.models.Item import Item


class StrictBaseModel(SQLModel):  # noqa: D101
    class Config(ConfigDict):  # noqa: D106
        strict = True


class Dummy(BaseModel):
    name: str


class HTTPError(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }


class CharacterStats(SQLModel):
    """Character stats model."""

    stat_combat: PositiveInt
    stat_dodge_rating: PositiveInt
    stat_hit_rating: PositiveInt
    stat_intelligence: PositiveInt
    stat_luck: PositiveInt
    stat_vitality: PositiveInt


class SpeciesBase(CharacterStats):
    """
    Species base model.

    Inherit from CharacterStats to have the same stats in Species and Character.

    Attributes
        name (str): The name of the species.
        description (str): The description of the species.
        icon (str): The icon of the species.
        base_strength (PositiveInt): The base strength of the species.
        base_dexterity (PositiveInt): The base dexterity of the species.
        base_intelligence (PositiveInt): The base intelligence of the species.

    """

    name: str = Field(default=None, unique=True, index=True)
    description: str = Field(default=None)
    icon: str
    base_strength: PositiveInt
    base_dexterity: PositiveInt
    base_intelligence: PositiveInt


class Species(SpeciesBase, table=True):
    """Species model."""

    id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )


class SpeciesCreate(SpeciesBase):
    """Species create model."""


class SpeciesRead(SpeciesBase):
    """Species read model."""

    id: uuid.UUID


class CharacterBase(CharacterStats):
    """
    Character base model.

    Inherit from CharacterStats to have the same stats in Species and Character.

    Attributes
        species (uuid.UUID): The species of the character.
        name (str): The name of the character.
        surname (str): The surname of the character.
        level (PositiveInt): The level of the character.
        experience (PositiveInt): The experience of the character.
        energy (PositiveInt): The energy of the character.
        inventory_id (uuid.UUID): The inventory ID of the character.
        strength (PositiveInt): The strength of the character.
        dexterity (PositiveInt): The dexterity of the character.
        intelligence (PositiveInt): The intelligence of the character.

    """

    # account_id: uuid.UUID = Field(default=None, foreign_key="accounts.id")  # noqa: ERA001
    species: uuid.UUID = Field(foreign_key="species.id")
    name: str
    surname: str
    level: PositiveInt
    experience: PositiveInt
    energy: PositiveInt
    strength: PositiveInt
    dexterity: PositiveInt
    intelligence: PositiveInt


class Character(CharacterBase, table=True):  # noqa: D101
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    inventory_id: uuid.UUID = Field(foreign_key="inventory.id")


class CharacterCreate(CharacterBase):
    """Character create model."""

    # inventory_id: uuid.UUID | None = None


class CharacterRead(CharacterBase):
    """Character read model."""

    id: uuid.UUID
    inventory_id: uuid.UUID


class InventoryExtension(SQLModel, table=True):  # noqa: D101
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        unique=True,
    )
    slots: PositiveInt
    name: str = Field(max_length=50, unique=True, index=True)
    description: str
    icon: str


class InventoryItemLink(SQLModel, table=True):
    inventory_id: uuid.UUID = Field(foreign_key="inventory.id", primary_key=True)
    item_id: uuid.UUID = Field(foreign_key="item.id", primary_key=True)
    item_count: PositiveInt


class InventoryBase(SQLModel):  # noqa: D101
    slots: NonNegativeInt = Field(default=10)
    gold: NonNegativeInt = Field(default=0)


class InventoryCreate(InventoryBase):  # noqa: D101
    pass


class InventoryRead(InventoryBase):  # noqa: D101
    id: uuid.UUID
    items: list["Item"]


class Inventory(InventoryBase, table=True):  # noqa: D101
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        unique=True,
    )
    items: list["Item"] = Relationship(
        back_populates="inventories",
        link_model=InventoryItemLink,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
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


class Item(ItemDamage, ItemRequirements, table=True):  # noqa: D101
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=50, unique=True, index=True)
    type: str
    description: str
    stackable: bool
    max_stack: PositiveInt
    unique_store: bool
    unique_equipped: bool
    icon: str
    inventories: list["Inventory"] = Relationship(
        back_populates="items",
        link_model=InventoryItemLink,
    )


class Monster(SQLModel, table=True):  # noqa: D101
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        unique=True,
    )
    name: str = Field(max_length=50, unique=True, index=True)
    description: str
    level: PositiveInt
    base_damage: PositiveInt
    icon: str


class Planet(SQLModel, table=True):
    """Planet model."""  # noqa: D203

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        unique=True,
    )
    name: str = Field(max_length=50, unique=True, index=True)
    description: str
    icon: str
