import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd


import time

def load_config(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)
    
config = load_config('siautt.json')
browser_name = config['browser']['name']


if browser_name == 'chrome':
    driver = webdriver.Chrome()
else:
    raise ValueError("Navegador no soportado: " + browser_name)

# Navegar a la URL base
base_url = config['url']['base_url']
driver.get(base_url)
wait = WebDriverWait(driver, 10)
try:
    # Encontrar los campos de email y contraseña e ingresar las credenciales

    email_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    email_field.send_keys(config['credentials']['email'])
    password_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))
    password_field.send_keys(config['credentials']['password'])
    entrar_button = driver.find_element(By.XPATH, "//button[contains(@type, 'submit')]")
    entrar_button.click() 
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Mi Espacio')]")))

    # Encontrar la etiqueta <a> que contiene un <span> con el texto "Mi Espacio"
    mi_espacio_link = driver.find_element(By.XPATH, "//a[.//span[contains(text(), 'Mi Espacio')]]")
    mi_espacio_link.click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Académico')]")))
    academico_link = driver.find_element(By.XPATH, "//a[.//span[contains(text(), 'Académico')]]")
    academico_link.click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Mis Calificaciones')]")))
    mis_calificaciones_link = driver.find_element(By.XPATH, "//a[.//span[contains(text(), 'Mis Calificaciones')]]")
    mis_calificaciones_link.click()
    
    wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'page-tabs')]")))
    historial_academico_link = wait.until(EC.visibility_of_element_located((By.ID, 'OConsultarCalificaciones')))
    historial_academico_link.click()
    tbody = driver.find_element(By.CSS_SELECTOR, "#TablaHistorico tbody")
    
    rows = tbody.find_elements(By.TAG_NAME, "tr")
    data = []
    for row in rows:
        # Extraer todas las celdas de la fila actual
        cells = row.find_elements(By.TAG_NAME, "td")
        # Extraer el texto de cada celda y agregarlo a la lista de datos
        row_data = [cell.text for cell in cells]
        data.append(row_data)

    df = pd.DataFrame(data)

# Especificar el nombre de las columnas si es necesario
# df.columns = ['Columna1', 'Columna2', 'Columna3', ...]

# Guardar el DataFrame en un archivo Excel
    df.to_excel("datos_extraidos.xlsx", index=False)
    
except Exception as e:
    print(f"Se ha producido un error: {e}")
time.sleep(180)

# Cerrar el navegador
driver.quit()