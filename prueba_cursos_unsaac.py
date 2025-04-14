'''
lista_cursos = ["IF619AIN", "IF061AIN", "IF662AIN", "IF616AIN"]
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time
# importar sqlite
import sqlite3

driver = webdriver.Chrome()
driver.get("http://ccomputo.unsaac.edu.pe/?op=alcurso")

# Buscar el curso
barra_busqueda = driver.find_element(By.NAME, "curso")
barra_busqueda.send_keys("IF619AIN")
barra_busqueda.send_keys(Keys.RETURN)

# Esperar un poquito por si demora en cargar
time.sleep(2)

# Obtener todas las tablas
tablas = driver.find_elements(By.CLASS_NAME, "ttexto")

# === Extraer info del curso ===
tabla_info = tablas[-2]  # Esta tabla está justo antes de la tabla de estudiantes
soup_info = BeautifulSoup(tabla_info.get_attribute("outerHTML"), "html.parser")

info = {}
filas_info = soup_info.find_all("tr")
for fila in filas_info:
    celdas = fila.find_all("td")
    for i in range(0, len(celdas), 2):
        clave = celdas[i].text.strip().replace(":", "")
        valor = celdas[i+1].text.strip()
        info[clave] = valor

# === Extraer estudiantes ===
tabla_estudiantes = tablas[-1]
soup_tabla = BeautifulSoup(tabla_estudiantes.get_attribute("outerHTML"), "html.parser")

filas = soup_tabla.find_all("tr")
data = []
for fila in filas[1:]:
    celdas = fila.find_all("td")
    if len(celdas) >= 3:
        codigo = celdas[1].text.strip()
        nombre = celdas[2].text.strip()
        data.append([codigo, nombre])

df = pd.DataFrame(data, columns=["Código", "Nombre"])

# Mostrar resultados
print("Información del curso:")
for clave, valor in info.items():
    print(f"  {clave}: {valor}")

print("Estudiantes:")
print(df.head())

driver.quit()
