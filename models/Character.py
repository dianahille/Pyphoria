import helper.files
import uuid

from typing import Self


# from pydantic import BaseModel, PositiveInt

# class CharacterModel(BaseModel):
#     id: uuid.UUID
#     name: str
#     surname: str
#     level: PositiveInt
#     experience: PositiveInt
#     energy: PositiveInt
#     gold: PositiveInt
#     inventory: list


class Model:
    def __init__(self: Self, account_id: uuid) -> None:
        """Initialize the class with the account_id and the data_file_name. If the file does not exist, create it."""
        self.account_id: uuid = account_id
        self.data_file_name: str = f"data/characters-{self.account_id}.json"
        helper.files.create_path_and_file(self.data_file_name)
        self.data = helper.files.read_json(self.data_file_name)

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
        self.data[character_id] = {
            "id": character_id,
            "name": name,
            "surname": surname,
            "level": 1,
            "experience": 0,
            "energy": 10,
            "gold": 0,
            "inventory": [],
        }
        self.save()

    def load(self: Self, character_id: uuid) -> dict:
        """Return the character with the character_id passed as argument."""
        return self.data[character_id]

    def save(self: Self) -> None:
        """Save the data to the file."""
        helper.files.write_json(self.data_file_name, self.data)

    def get_full_name(self: Self, character_id: uuid) -> str:
        """Return the full name of the character with the character_id passed as argument."""
        character = self.data[character_id]
        return f"{character['name']} {character['surname']}"
