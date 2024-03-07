import helper.files

class Character:
    def __init__(self) -> None:
        self.data_file_name = 'data/characters.json'

        self.data_file_handle = open(self.data_file_name, 'r')
        self.data = json.load(self.data_file_handle)