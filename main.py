from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Json import Json
from WebScrapper import WebScrapper
from excel import Excel
import time

def main(config_file):
    exel_config = Json(config_file)
    config = exel_config.get_config()

    scrapper = WebScrapper()

    try:
        scrapper.load_page(config['search_url'])

        for action in config['actions']:
            scrapper.perform_action(action)
            time.sleep(1)
    except Exception as e:
        print(f"An error occurred while performing actions: {e}")
        scrapper.close()

if __name__ == "__main__":
    config_file = "examen.json"  # Cambia el nombre del archivo JSON según sea necesario
    main(config_file)