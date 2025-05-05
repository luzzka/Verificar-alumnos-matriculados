import requests
import re
from bs4 import BeautifulSoup

# extraer el texto de temp_data.txt
texto = ""
with open("temp_data.txt", "r", encoding="utf-8") as file:
    texto = file.read()

'''
# Usar una expresión regular para encontrar los códigos de los cursos
courses = re.findall(r'\b[A-Z]{2}\d{3}[A-Z]IN\b', texto)

# eliminar duplicados
#courses = list(set(courses))

# mostrar los cursos
print(len(courses))
'''

# Parsear el HTML
soup = BeautifulSoup(texto, "html.parser")

# Encontrar todas las filas de la tabla
rows = soup.find_all("tr", style=lambda value: value and "background-color:#F0F0F0" in value)

# Lista para almacenar los códigos de los cursos
course_codes = []

# Recorrer las filas y extraer los códigos de los cursos
for row in rows:
    cells = row.find_all("td")
    coure_code = cells[1].get_text(strip=True)
    course_codes.append(coure_code)

# Mostrar los códigos de los cursos
print(course_codes)