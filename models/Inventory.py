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
    def __init__(self: Self, character_id: uuid) -> None:
        """Initialize the class with the data_file_name. If the file does not exist, create it."""
        self.data_file_name: str = f"data/inventories/inventory-{character_id}.json"
        self.character_id: uuid = character_id
        helper.files.create_path_and_file(self.data_file_name)
        self.data = helper.files.read_json(self.data_file_name)
        self.base_inventory_data = {
            "items": [],
            "gold": 0,
        }
        if self.data == {}:
            self.data = self.base_inventory_data
            self.data["inventory_id"] = str(uuid.uuid4())
            self.data["character_id"] = self.character_id
            self.save()

    def modify(self: Self) -> None:
        """Modify the item with the item_id passed as argument."""
        # TODO add data verfication using pydantic
        pass
        self.save()

    def load(self: Self) -> dict:
        """Return the monster with the monster_id passed as argument."""
        return self.data

    def save(self: Self) -> None:
        """Save the data to the file."""
        helper.files.write_json(self.data_file_name, self.data)
