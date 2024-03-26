import json  # noqa: D100
import os

# _filepath = Path(__file__)  # noqa: ERA001
# pyphoria_path = Path.parent(Path.parent(Path.resolve(Path(_filepath))))  # noqa: ERA001
# print(pyphoria_path)  # noqa: ERA001
# def create_path_and_file(file_name: str) -> None:
#     print(f"{pyphoria_path}/{Path.parent(file_name)}")  # noqa: ERA001
#     if not Path.exists(f"{pyphoria_path}/{Path.parent(file_name)}"):
#         Path.mkdir(Path(f"{pyphoria_path}/{Path.parent(file_name)}"), create_parents=True)  # noqa: ERA001
#     if not Path.exists(f"{pyphoria_path}/{file_name}"):
#         open(f"{pyphoria_path}/{file_name}", "w").close()  # noqa: ERA001
# def read_json(file_name: str) -> dict:
#     with open(f"{pyphoria_path}/{file_name}", "r") as file:
#         try:  # noqa: ERA001
#             data = json.load(file)  # noqa: ERA001
#         except json.decoder.JSONDecodeError:  # noqa: ERA001
#             data = {}  # noqa: ERA001
#     return data  # noqa: ERA001
# def write_json(file_name: str, data: dict) -> None:
#     with open(f"{pyphoria_path}/{file_name}", "w") as file:
#         json.dump(data, file, indent=4)  # noqa: ERA001

pyphoria_path = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)  # noqa: PTH100, PTH120


def create_path_and_file(file_name: str) -> None:  # noqa: D103
    if not os.path.exists(
        f"{pyphoria_path}/{os.path.dirname(file_name)}"
    ):  # noqa: PTH110, PTH120
        os.makedirs(
            f"{pyphoria_path}/{os.path.dirname(file_name)}"
        )  # noqa: PTH103, PTH120
    if not os.path.exists(f"{pyphoria_path}/{file_name}"):  # noqa: PTH110
        open(f"{pyphoria_path}/{file_name}", "w").close()


def read_json(file_name: str) -> dict:  # noqa: D103
    with open(f"{pyphoria_path}/{file_name}", "r") as file:
        try:
            data = json.load(file)
        except json.decoder.JSONDecodeError:
            data = {}
    return data


def write_json(file_name: str, data: dict) -> None:  # noqa: D103
    with open(f"{pyphoria_path}/{file_name}", "w") as file:
        json.dump(data, file, indent=4, default=str)
