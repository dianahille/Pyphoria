import json
import os

pyphoria_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_path_and_file(file_name: str) -> None:
    if not os.path.exists(f"{pyphoria_path}/{os.path.dirname(file_name)}"):
        os.makedirs(f"{pyphoria_path}/{os.path.dirname(file_name)}")
    open(f"{pyphoria_path}/{file_name}", 'w').close()


