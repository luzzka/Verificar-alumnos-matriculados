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
        "curso": course_code.upper(),  # Course code field name. Using upper() to ensure uppercase.
        "semestre": semester,       # Semester field name.
        "Consultar": "Consultar"   # Submit button name and value.
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

# Example usage
course_code = "IF616AIN"
course_codes = [
    'IF619AIN', 'IF061AIN', 'IF662AIN', 'IF616AIN', 'IF484AIN', 'ME359ZIN', 'ME358ZIN', 'IF553AIN', 'IF653AIN', 
    'IF554AIN', 'IF556AIN', 'IF618ZIN', 'MEG01AIN', 'MEG01BIN', 'MEG02AIN', 'MEG02BIN', 'CBG01AIN', 'CBG01BIN', 
    'FIG01AIN', 'FIG01BIN', 'HIG01AIN', 'HIG01BIN', 'QUG01AIN', 'QUG01BIN', 'ME903AIN', 'MEG04AIN', 'MEG04BIN', 
    'MEG03AIN', 'MEG03BIN', 'IFI01AIN', 'IFI01BIN', 'LCG01AIN', 'LCG01BIN', 'MEI04AIN', 'MEI04BIN', 'IFG01AIN', 
    'IFG01BIN', 'IF450AIN', 'ME351AIN', 'MEI05AIN', 'MEI05BIN', 'IFI02AIN', 'IFI02BIN', 'ME350AIN', 'MEI09AIN', 
    'FI370AIN', 'FII02AIN', 'FII02BIN', 'MEI06AIN', 'ME352AIN', 'IF451AIN', 'IFI03AIN', 'IFI03BIN', 'IF480AIN', 
    'IF452AIN', 'IF452BIN', 'EL371AIN', 'EL371BIN', 'ME354AIN', 'ME354BIN', 'ME355AIN', 'IF060AIN', 'IF453AIN', 
    'IF453BIN', 'IF610AIN', 'IF610BIN', 'ME356AIN', 'ME356BIN', 'IF481AIN', 'IF481BIN', 'IF650AIN', 'IF550AIN', 
    'IF550BIN', 'IF454AIN', 'IF454BIN', 'IF455AIN', 'IF455BIN', 'IF458AIN', 'IF458BIN', 'IF612AIN', 'IF612BIN', 
    'IF611AIN', 'IF611BIN', 'IF457AIN', 'IF457BIN', 'IF551AIN', 'IF551BIN', 'IF456AIN', 'IF456BIN', 'IF467AIN', 
    'IF466AIN', 'IF613AIN', 'IF613BIN', 'IF651AIN', 'IF651BIN', 'IF063AIN', 'IF552AIN', 'IF552BIN', 'IF652AIN', 
    'IF664AIN', 'IF664BIN', 'IF614AIN', 'IF669AIN', 'IF482AIN', 'IF710AIN', 'IF710BIN', 'IF459AIN', 'IF062AIN', 
    'IF483AIN', 'IF617AIN', 'IF656AIN', 'IF654AIN', 'IF657AIN', 'IF711AIN', 'IF711BIN']
semester_value = "2025-1" # You can change the semester
students = get_students_for_course(course_code, semester_value) #Send the semester
if students:
    print(f"Students for {course_code} in {semester_value}: {students}")