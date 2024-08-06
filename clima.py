from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

# Initialize WebDriver
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

# URL to scrape
url = 'https://www.meteored.mx/clima_Torreon-America+Norte-Mexico-Coahuila-MMTC-1-22375.html'
driver.get(url)

# Locate the section containing the daily forecasts
try:
    section = wait.until(EC.presence_of_element_located((By.XPATH, "//section[@class='dias card_struct']")))
    forecasts = section.find_elements(By.CLASS_NAME, 'grid-item')

    forecast_data = []

    for forecast in forecasts:
        day = forecast.find_element(By.CLASS_NAME, 'text-0').text
        temperature_max = forecast.find_element(By.CLASS_NAME, 'max').text
        temperature_min = forecast.find_element(By.CLASS_NAME, 'min').text
        
        forecast_data.append({
            'day': day,
            'temperature_max': temperature_max,
            'temperature_min': temperature_min,
        })

    # Print the extracted data
    for data in forecast_data:
        print(f"Day: {data['day']}")
        print(f"Temperature Max: {data['temperature_max']}")
        print(f"Temperature Min: {data['temperature_min']}")
        print("---")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
