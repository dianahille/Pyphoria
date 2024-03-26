import uuid
from typing import Self

import pyphoria
from pyphoria.models import Item


class Model:
    def __init__(self: Self, character_id: uuid) -> None:
        """Initialize the class with the data_file_name. If the file does not exist, create it."""
        self.data_file_name: str = f"data/inventories/inventory-{character_id}.json"
        self.character_id: uuid = character_id
        pyphoria.helper.files.create_path_and_file(self.data_file_name)
        self.data = pyphoria.helper.files.read_json(self.data_file_name)
        self.base_inventory_data = {
            "slots": 10,
            "items": [],
            "gold": 0,
        }
        if self.data == {}:
            self.data = self.base_inventory_data
            self.data["inventory_id"] = str(uuid.uuid4())
            self.data["character_id"] = self.character_id
            self.save()

    def check_open_slots(self: Self) -> int:
        """Return true if the inventory has open slots."""
        if len(self.data["items"]) < self.data["slots"]:
            return True
        return False

    def add(self: Self, item_id: uuid, amount: int = 1) -> None:
        """Modify the item with the item_id passed as argument."""
        # TODO add data verfication using pydantic  # noqa: FIX002, TD002, TD003, TD004
        item_c = Item()
        item = item_c.load(item_id)
        if self.check_stored(item_id):
            if item["stackable"]:
                if self.data["items"][item_id]["amount"] + amount < item["max_stack"]:
                    self.data["items"][item_id]["amount"] += amount
                    self.save()
                    return
                else:
                    self.data["items"][item_id]["amount"] = item["max_stack"]
                    self.save()
                    return
            elif item["unique_store"]:
                print("Item is unique.")

        if self.check_open_slots():
            self.data["items"][item_id] = {"item_id": item_id, "amount": amount}
        self.save()

    def check_stored(self: Self, item_id: uuid) -> bool:
        """Check if the item is stored in the inventory."""
        if item_id in self.data["items"]:
            return True
        return False

    def load(self: Self) -> dict:
        """Return the monster with the monster_id passed as argument."""
        return self.data

    def save(self: Self) -> None:
        """Save the data to the file."""
        pyphoria.helper.files.write_json(self.data_file_name, self.data)
