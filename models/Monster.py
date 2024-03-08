import helper.files
import uuid

from typing import Self


# from pydantic import BaseModel, PositiveInt

# class MonsterModel(BaseModel):
#     id: uuid.UUID
#     name: str
#     description: str
#     level: PositiveInt
#     experience: PositiveInt
#     gold: PositiveInt


class Model:
    def __init__(self: Self) -> None:
        """Initialize the class with the account_id and the data_file_name. If the file does not exist, create it."""
        self.data_file_name: str = f"data/monsters.json"
        helper.files.create_path_and_file(self.data_file_name)
        self.data = helper.files.read_json(self.data_file_name)

    def create(
        self: Self,
        name: str,
        description: str,
        level: int = 1,
        base_damage: int = 1,
        icon: str = "",
    ) -> None:
        """Create a new monster."""
        monster_id = str(uuid.uuid4())
        self.data[monster_id] = {
            "id": monster_id,
            "name": name,
            "description": description,
            "level": level,
            "base_damage": base_damage,
            "icon": icon,
        }
        self.save()

    def modify(self: Self, monster_id: uuid, monster_data: dict) -> None:
        """Modify the monster with the monster_id passed as argument."""
        # TODO add data verfication using pydantic
        monster_data.delete("monster_id")
        self.data[monster_id].update(monster_data)
        self.save()

    def load(self: Self, monster_id: uuid) -> dict:
        """Return the monster with the monster_id passed as argument."""
        return self.data[monster_id]

    def save(self: Self) -> None:
        """Save the data to the file."""
        helper.files.write_json(self.data_file_name, self.data)
