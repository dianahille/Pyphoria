import json
import os

# _filepath = Path(__file__)
# pyphoria_path = Path.parent(Path.parent(Path.resolve(Path(_filepath))))
# print(pyphoria_path)
# def create_path_and_file(file_name: str) -> None:
#     print(f"{pyphoria_path}/{Path.parent(file_name)}")
#     if not Path.exists(f"{pyphoria_path}/{Path.parent(file_name)}"):
#         Path.mkdir(Path(f"{pyphoria_path}/{Path.parent(file_name)}"), create_parents=True)
#     if not Path.exists(f"{pyphoria_path}/{file_name}"):
#         open(f"{pyphoria_path}/{file_name}", "w").close()
# def read_json(file_name: str) -> dict:
#     with open(f"{pyphoria_path}/{file_name}", "r") as file:
#         try:
#             data = json.load(file)
#         except json.decoder.JSONDecodeError:
#             data = {}
#     return data
# def write_json(file_name: str, data: dict) -> None:
#     with open(f"{pyphoria_path}/{file_name}", "w") as file:
#         json.dump(data, file, indent=4)

pyphoria_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_path_and_file(file_name: str) -> None:
    if not os.path.exists(f"{pyphoria_path}/{os.path.dirname(file_name)}"):
        os.makedirs(f"{pyphoria_path}/{os.path.dirname(file_name)}")
    if not os.path.exists(f"{pyphoria_path}/{file_name}"):
        open(f"{pyphoria_path}/{file_name}", "w").close()


def read_json(file_name: str) -> dict:
    with open(f"{pyphoria_path}/{file_name}", "r") as file:
        try:
            data = json.load(file)
        except json.decoder.JSONDecodeError:
            data = {}
    return data


def write_json(file_name: str, data: dict) -> None:
    with open(f"{pyphoria_path}/{file_name}", "w") as file:
        json.dump(data, file, indent=4, default=str)
