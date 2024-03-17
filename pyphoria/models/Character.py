import uuid
from typing import Self

from pydantic import PositiveInt
from sqlmodel import Field

import pyphoria.helper.files
from models import StrictBaseModel
from models.Inventory import Model as Inventory


class CharacterStatsModel(StrictBaseModel, table=False):
    vitality: PositiveInt
    luck: PositiveInt
    intelligence: PositiveInt
    combat: PositiveInt
    hit_rating: PositiveInt
    dodge_rating: PositiveInt


class SpeciesModel(StrictBaseModel, table=True):
    name: str = Field(default=None, primary_key=True)
    description: str
    icon: str
    base_strength: PositiveInt
    base_dexterity: PositiveInt
    base_intelligence: PositiveInt


class CharacterModel(StrictBaseModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    account_id: uuid.UUID = Field(default=None, foreign_key="accounts.id")
    species: uuid.UUID = Field(default=None, foreign_key="species.name")
    name: str
    surname: str
    level: PositiveInt = 1
    experience: PositiveInt = 0
    energy: PositiveInt
    inventory: uuid.UUID = Field(default=None, foreign_key="inventory.inventory_id")
    strength: PositiveInt
    dexterity: PositiveInt
    intelligence: PositiveInt
    stats: CharacterStatsModel


class Model:
    def __init__(self: Self, account_id: uuid) -> None:
        """Initialize the class with the account_id and the data_file_name. If the file does not exist, create it."""
        self.account_id: uuid = account_id
        self.data_file_name: str = f"data/characters/characters-{self.account_id}.json"
        pyphoria.helper.files.create_path_and_file(self.data_file_name)
        self.data = pyphoria.helper.files.read_json(self.data_file_name)
        self.base_character_data = {
            "account_id": self.account_id,
            "level": 1,
            "experience": 0,
            "energy": 10,
            "base_stats": {"strength": 1, "dexterity": 1, "intelligence": 1},
        }

    def check_name_available(self: Self, name: str, surname: str) -> bool:
        """Iterate over the items in the dictionary and check if the full name of the character is equal to the name and surname passed as arguments. If it is, return False. If the loop finishes, return True."""
        for character_id in self.data.items():
            if (
                f"{self.get_full_name(character_id=character_id)}"
                == f"{name} {surname}"
            ):
                return False
        return True

    def create(self: Self, name: str, surname: str) -> None:
        """Create a new character."""
        if not self.check_name_available(name, surname):
            print("Name already taken.")
            return
        character_id = str(uuid.uuid4())
        inventory = Inventory(character_id)
        self.data[character_id] = {
            "character_id": character_id,
            "name": name,
            "surname": surname,
            "inventory": inventory.data["inventory_id"],
            **self.base_character_data,
        }
        self.save()

    def modify(self: Self, character_id: uuid, character_data: dict) -> None:
        """Modify the character with the character_id passed as argument."""
        # TODO add data verfication using pydantic
        character_data.delete("character_id")
        self.data[character_id].update(character_data)
        self.save()

    def load(self: Self, character_id: uuid) -> dict:
        """Return the character with the character_id passed as argument."""
        return self.data[character_id]

    def save(self: Self) -> None:
        """Save the data to the file."""
        pyphoria.helper.files.write_json(self.data_file_name, self.data)

    def get_full_name(self: Self, character_id: uuid) -> str:
        """Return the full name of the character with the character_id passed as argument."""
        character = self.data[character_id]
        return f"{character['name']} {character['surname']}"
