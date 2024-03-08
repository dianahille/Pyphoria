import helper.files
import uuid

from typing import Self
from pprint import pprint as pp


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
        self.data_file_name: str = f"data/monsters.json"
        helper.files.create_path_and_file(self.data_file_name)
        self.data = helper.files.read_json(self.data_file_name)

    def create(self: Self, name: str, description: str) -> None:
        monster_id = str(uuid.uuid4())
        self.data[monster_id] = {
            "id": monster_id,
            "name": name,
            "description": description,
            "level": 1,
            "experience": 0,
            "gold": 0,
        }
        self.save()

    def load(self: Self, monster_id: uuid) -> dict:
        return self.data[monster_id]

    def save(self: Self) -> None:
        helper.files.write_json(self.data_file_name, self.data)
