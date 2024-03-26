import uuid  # noqa: N999, D100
from typing import Self

import pyphoria


class Model:
    def __init__(self: Self) -> None:
        """Initialize the class with the data_file_name. If the file does not exist, create it."""
        self.data_file_name: str = "data/items.json"
        pyphoria.helper.files.create_path_and_file(self.data_file_name)
        self.data = pyphoria.helper.files.read_json(self.data_file_name)
        self.base_item_data = {
            "type": "weapon",
            "stackable": False,
            "max_stack": 100,
            "unique_store": False,
            "unique_equipped": False,
            "requirements": {
                "level": 1,
                "strength": 1,
                "dexterity": 1,
                "intelligence": 1,
            },
            "base_damage": {"physical": {"min": 1, "max": 1}},
            "icon": "",
        }

    def create(
        self: Self,
        name: str,
        description: str,
        item_data: dict = {},
    ) -> None:
        """Create a new monster."""
        item_id = str(uuid.uuid4())
        _item_data = self.base_item_data.copy()
        _item_data.update(item_data)
        self.data[item_id] = {
            "id": item_id,
            "name": name,
            "description": description,
            **_item_data,
        }
        self.save()

    def modify(self: Self, item_id: uuid, item_data: dict) -> None:
        """Modify the item with the item_id passed as argument."""
        # TODO add data verfication using pydantic  # noqa: FIX002, TD002, TD003, TD004
        item_data.delete("item_id")
        self.data[item_id].update(item_data)
        self.save()

    def load(self: Self, item_id: uuid) -> dict:
        """Return the Item with the item_id passed as argument."""
        return self.data[item_id]

    def save(self: Self) -> None:
        """Save the data to the file."""
        pyphoria.helper.files.write_json(self.data_file_name, self.data)
