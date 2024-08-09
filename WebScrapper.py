from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from excel import Excel

class WebScrapper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 30)
        self.data = []

    def load_page(self, url):
        self.driver.get(url)
        self.driver.fullscreen_window()

    def find_element(self, selector):
        try:
            return self.wait.until(EC.presence_of_element_located(selector))
        except Exception as e:
            print(f"An error occurred while finding element: {selector}")
            print(e)
    
    def perform_action(self, action):
        try:
            selector = (getattr(By, action['selector_type'].upper()), action['selector_value'])
            action_type = action['action_type']

            if action_type == 'input':
                element = self.find_element(selector)
                element.send_keys(action.get('value'))
            elif action_type == 'click':
                element = self.find_element(selector)
                element.click()
            elif action_type == 'wait':
                self.find_element(selector)
            elif action_type == 'find':
                self.find_element(selector)
            elif action_type == 'extract':
                self.extract_data(selector, action['row_selector'], action['columns'], action['output_file'], action.get('append', False))
            elif action_type == 'enter':
                element = self.find_element(selector)
                element.send_keys(Keys.ENTER)
            elif action_type == 'scroll':
                if 'pixels' in action:
                    self.driver.execute_script(f"window.scrollBy(0, {action['pixels']});")
                else:
                    element = self.find_element(selector)
                    self.driver.execute_script("arguments[0].scrollIntoView();", element)
            elif action_type == 'upload':
                element = self.find_element(selector)
                element.send_keys(action.get('value')) 
        except Exception as e:
            print(f"An error occurred while performing action: {action}")
            print(e)

    def extract_data(self, structure_selector, row_selector, columns, output_file, append=False):
        try:
            structure_element = self.find_element(structure_selector)
            
            # Try finding rows using the primary XPath selector
            rows = structure_element.find_elements(By.XPATH, row_selector)
            
            # If no rows are found, attempt an alternative strategy
            if not rows:
                print("Primary XPath row selector failed, trying alternative selectors...")
                # Example alternative strategy: use a different CSS selector or XPath
                alternative_selectors = [
                    (By.CSS_SELECTOR, "li.ProductCard"),  # Adjust selector as needed
                    (By.XPATH, ".//div[@class='ProductListPage CategoryProductList-Page']//li")  # Adjust selector as needed
                ]
                
                for alt_selector in alternative_selectors:
                    try:
                        rows = structure_element.find_elements(*alt_selector)
                        if rows:
                            break
                    except Exception as e:
                        print(f"An error occurred while trying alternative selector: {alt_selector}")
                        print(e)
                
            # If still no rows are found, raise an error
            if not rows:
                raise Exception("Failed to find rows using all provided selectors.")
            
            # Process the rows as usual
            data = []
            for row in rows:
                row_data = {}
                for col in columns:
                    col_name = col['name']
                    try:
                        if 'selector_type' in col and 'selector_value' in col:
                            col_selector = (getattr(By, col['selector_type'].upper()), col['selector_value'])
                            cell = row.find_element(*col_selector)
                            row_data[col_name] = cell.text.strip()
                        elif 'index' in col:
                            cells = row.find_elements(By.XPATH, "./*")
                            col_index = col['index']
                            if col_index < len(cells):
                                row_data[col_name] = cells[col_index].text.strip()
                            else:
                                row_data[col_name] = None
                    except Exception as e:
                        print(f"An error occurred while extracting column {col_name} in row: {row.text}")
                        print(e)
                        row_data[col_name] = None
                data.append(row_data)

            # Export data to Excel
            exporter = Excel(data)
            exporter.export_to_excel(output_file, append)

        except Exception as e:
            print(f"An error occurred while extracting data")
            print(e)
    
    def get_data(self):
        try:
            return self.data
        except Exception as e:
            print(f"An error occurred while getting data")
            print(e)

    def close(self):
        self.driver.quit()
