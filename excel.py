import pandas as pd

class Excel:
    def __init__(self, data):
        self.data = data

    def export_to_excel(self, file_path):
        df = pd.DataFrame(self.data)
        df.to_excel(file_path, index=False)
