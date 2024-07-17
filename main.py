from Json import Json
from excel import Excel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class WebScrapper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.data = []

    def load_page(self, url):
        self.driver.get(url)
        time.sleep(5)

    def find_element(self, selector):
        return self.wait.until(EC.presence_of_element_located(selector))

    def perform_action(self, selector, action_type, value=None):
        try:
            element = self.find_element(selector)
            if action_type == 'input':
                element.send_keys(value)
            elif action_type == 'click':
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                self.wait.until(EC.element_to_be_clickable(selector))
                element.click()
            elif action_type == 'wait':
                self.find_element(selector)
        except TimeoutException:
          print(f"Timeout al intentar realizar {action_type} en {selector}")
        except Exception as e:
         print(f"Error en la acción {action_type}: {e}")

    def fetch_data_structure(self, structure_selector, row_selector, columns):
            structure_element = self.find_element(structure_selector)
            rows = structure_element.find_elements(By.CSS_SELECTOR, row_selector)

            for row in rows:
                row_data = {}
                cells = row.find_elements(By.XPATH, "./*")

                for col in columns:
                    col_name = col['name']
                    col_index = col['index']
                    if col_index < len(cells):
                        row_data[col_name] = cells[col_index].text.strip()
                    else:
                        row_data[col_name] = None  # Manejo de celdas faltantes

                self.data.append(row_data)



    def get_data(self):
        return self.data

    def close(self):
        self.driver.quit()

def main(config_file):
    exel_config = Json(config_file)
    config = exel_config.get_config()

    scrapper = WebScrapper()

    try:
        scrapper.load_page(config['search_url'])

        for action in config['actions']:
            selector = (getattr(By, action['selector_type'].upper()), action['selector_value'])
            scrapper.perform_action(selector, action['action_type'], action.get('value'))
            time.sleep(1)

        structure_selector = (getattr(By, config['data_structure']['selector_type'].upper()), config['data_structure']['selector_value'])
        row_selector = config['data_structure']['row_selector']
        columns = config['data_structure']['columns']

        scrapper.fetch_data_structure(structure_selector, row_selector, columns)
        data = scrapper.get_data()

        exporter = Excel(data)
        exporter.export_to_excel(config['output_file'])
    finally:
        scrapper.close()

if __name__ == "__main__":
    config_file = "clima.json"
    main(config_file)
