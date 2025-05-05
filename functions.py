import requests
from bs4 import BeautifulSoup
import pandas as pd

# =============================================================================================================================================
def get_course_info(soup_text):
    """Extracts course information from the HTML soup."""
    # extract the 1st table
    soup = soup_text
    tablas = soup.find_all("table", class_="ttexto")
    tabla_info = tablas[-2]  
    
    info = {}
    filas_info = tabla_info.find_all("tr")
    for fila in filas_info:
        celdas = fila.find_all("td")
        for i in range(0, len(celdas), 2):
            clave = celdas[i].text.strip().replace(":", "")
            valor = celdas[i+1].text.strip()
            info[clave] = valor
    return info

# =============================================================================================================================================
def get_student_info(soup_text):
    """Extracts name and codes of students from the HTML soup."""
    # extract the 2nd table
    soup = soup_text
    tablas = soup.find_all("table", class_="ttexto")
    tabla_estudiantes = tablas[-1]
    
    filas = tabla_estudiantes.find_all("tr")
    data = []
    for fila in filas[1:]:
        celdas = fila.find_all("td")
        if len(celdas) >= 3:
            codigo = celdas[1].text.strip()
            nombre = celdas[2].text.strip()
            data.append([codigo, nombre])
    df = pd.DataFrame(data, columns=["Código", "Nombre"])
    return df

# =============================================================================================================================================
def get_students_for_course(course_code, semester="2025-1"): 
    """Extracts information of teachers and students from a given course."""
    url = "http://ccomputo.unsaac.edu.pe/index.php?op=alcurso"
    data = {
        "curso": course_code.upper(),  
        "semestre": semester,       
        "Consultar": "Consultar"   
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"  # Add user agent
    }

    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 200:
        # Check if the course is not found.
        if "No existe curso" in response.text:
            print("Course not found")
            return None 
        
        soup = BeautifulSoup(response.content, "html.parser")

        info_curso = get_course_info(soup)
        print("Información del curso:")
        for clave, valor in info_curso.items():
            print(f"  {clave}: {valor}")

        info_estudiantes = get_student_info(soup)
        print(info_estudiantes.head())
        
    else:
        print(f"Error: {response.status_code}")
        return None
