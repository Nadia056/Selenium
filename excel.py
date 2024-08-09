import openpyxl
import os

class Excel:
    def __init__(self, data):
        self.data = data

    def export_to_excel(self, filename, append=False):
        if append and os.path.exists(filename):
            workbook = openpyxl.load_workbook(filename)
            sheet = workbook.active
        else:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            headers = list(self.data[0].keys())  # Convertir dict_keys a lista
            sheet.append(headers)
        
        for row_data in self.data:
            sheet.append(list(row_data.values()))
        
        workbook.save(filename)
