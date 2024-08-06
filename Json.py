import json

class Json:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = self.load_json()

    def load_json(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def get_config(self):
        return self.config
