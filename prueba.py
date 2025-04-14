'''from selenium import webdriver
from selenium.webdriver.chrome.options import Options

option = webdriver.ChromeOptions()
driver = webdriver.Chrome(options = option)

driver.get('https://www.google.com/')

print("Título de la página:", driver.title)

driver.find_element()
driver.quit()'''


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Iniciar el navegador
driver = webdriver.Chrome()

# Ir a Google
driver.get("https://www.google.com")

# Aceptar cookies si aparece (opcional)
try:
    aceptar_btn = driver.find_element(By.XPATH, "//div[contains(text(),'Acepto')]")
    aceptar_btn.click()
except:
    pass  # Si no aparece, continúa normal

# Encontrar la barra de búsqueda (por su nombre "q")
barra_busqueda = driver.find_element(By.NAME, "q")

# Escribir algo en la barra
barra_busqueda.send_keys("Cusco Perú")

# Presionar Enter
barra_busqueda.send_keys(Keys.RETURN)

# Aceptar cookies si aparece (opcional)
try:
    aceptar_btn = driver.find_element(By.XPATH, "//div[contains(text(),'Acepto')]")
    aceptar_btn.click()
except:
    pass  # Si no aparece, continúa normal

# Esperar unos segundos para ver los resultados
time.sleep(5)

# Imprimir título de la página de resultados
print("Título después de buscar:", driver.title)

# Cerrar el navegador
driver.quit()
