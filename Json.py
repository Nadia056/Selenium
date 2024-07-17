import json

class Json:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self):
        with open(self.config_file, 'r') as file:
            return json.load(file)

    def get_config(self):
        return self.config
