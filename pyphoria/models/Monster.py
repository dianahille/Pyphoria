import uuid
from dataclasses import Field
from typing import Self

from pydantic import PositiveInt

import pyphoria.pyphoria.helper.files
from models import StrictBaseModel


class MonsterModel(StrictBaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    description: str
    level: PositiveInt
    base_damage: PositiveInt
    icon: str


class Model:
    def __init__(self: Self) -> None:
        """
        Initialize the class with the account_id and the data_file_name.

        If the file does not exist, create it.
        """
        self.data_file_name: str = "data/monsters.json"
        pyphoria.helper.files.create_path_and_file(self.data_file_name)
        self.data = pyphoria.helper.files.read_json(self.data_file_name)

    def create(
        self: Self,
        name: str,
        description: str,
        level: int = 1,
        base_damage: int = 1,
        icon: str = "",
    ) -> None:
        """Create a new monster."""
        monster_id = uuid.uuid4()
        self.data[str(monster_id)] = MonsterModel(
            id=monster_id,
            name=name,
            description=description,
            level=level,
            base_damage=base_damage,
            icon=icon,
        ).model_dump()
        self.save()

    def modify(self: Self, id: uuid, monster_data: dict) -> None:
        """Modify the monster with the monster_id passed as argument."""
        MonsterModel(id=id, **monster_data)
        self.data.pop(str(id), None)
        self.data[str(id)] = monster_data
        self.save()

    def load(self: Self, monster_id: uuid) -> dict:
        """Return the monster with the monster_id passed as argument."""
        return self.data[monster_id]

    def save(self: Self) -> None:
        """Save the data to the file."""
        pyphoria.helper.files.write_json(self.data_file_name, self.data)

    def list(self: Self) -> dict:
        """Return the list of monsters."""
        return self.data
