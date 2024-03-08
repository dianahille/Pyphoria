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
        """Initialize the class with the data_file_name. If the file does not exist, create it."""
        self.data_file_name: str = f"data/items.json"
        helper.files.create_path_and_file(self.data_file_name)
        self.data = helper.files.read_json(self.data_file_name)

    def create(
        self: Self,
        name: str,
        description: str,
        requirements: dict = {
            "level": 1,
            "strength": 1,
            "dexterity": 1,
            "intelligence": 1,
        },
        base_damage: dict = {"physical": {"min": 1, "max": 1}},
        icon: str = "",
    ) -> None:
        """Create a new monster."""
        item_id = str(uuid.uuid4())
        self.data[item_id] = {
            "id": item_id,
            "name": name,
            "description": description,
            "requirements": requirements,
            "base_damage": base_damage,
            "icon": icon,
        }
        self.save()

    def modify(self: Self, item_id: uuid, item_data: dict) -> None:
        """Modify the item with the item_id passed as argument."""
        # TODO add data verfication using pydantic
        item_data.delete("item_id")
        self.data[item_id].update(item_data)
        self.save()

    def load(self: Self, item_id: uuid) -> dict:
        """Return the monster with the monster_id passed as argument."""
        return self.data[item_id]

    def save(self: Self) -> None:
        """Save the data to the file."""
        helper.files.write_json(self.data_file_name, self.data)
