import pandas as pd
import openpyxl

class Excel:
    def __init__(self, data):
        self.data = data

    def export_to_excel(self, file_path):
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        if not self.data:
            return

        headers = list(self.data[0].keys())
        sheet.append(headers)

        for row in self.data:
            sheet.append([row.get(header, '') for header in headers])

        workbook.save(file_path)