import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Configuración Brave
brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
options = Options()
options.binary_location = brave_path

# Configuraciones para evitar detección
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

service = Service(r"C:\WebDrivers\chromedriver.exe")

driver = webdriver.Chrome(service=service, options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

try:
    # 1. Limpieza inicial
    driver.get("about:blank")
    time.sleep(2)
    driver.delete_all_cookies()
    
    # 2. Navegar a la página
    url = "https://www.espn.com.co/futbol/resultados"
    driver.get(url)
    print(f"URL cargada: {driver.current_url}")
    time.sleep(random.uniform(4, 6))
    
    # 3. Esperar a que carguen los partidos
    wait = WebDriverWait(driver, 20)
    
    # Esperar por el contenedor principal de partidos
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ScoreboardScoreCell")))
    
    # 4. Encontrar todos los partidos
    partidos = driver.find_elements(By.CSS_SELECTOR, ".ScoreboardScoreCell")
    print(f"Encontrados {len(partidos)} partidos")
    
    # Inicializar la lista para guardar los resultados
    resultados_partidos = []
    
    # 5. Procesar cada partido
    for i, partido in enumerate(partidos):
        try:
            equipos = partido.find_elements(By.CSS_SELECTOR, ".ScoreCell__TeamName.ScoreCell__TeamName--shortDisplayName.db")
            marcadores = partido.find_elements(By.CSS_SELECTOR, ".ScoreCell__Score")
            
            if len(equipos) >= 2 and len(marcadores) >= 2:
                equipo_local = equipos[0].text
                equipo_visitante = equipos[1].text
                marcador_local = marcadores[0].text
                marcador_visitante = marcadores[1].text
                
                # Almacenar en la lista solo si los marcadores son dígitos
                if marcador_local.isdigit() and marcador_visitante.isdigit():
                    resultados_partidos.append({
                        "equipo_local": equipo_local,
                        "marcador_local": marcador_local,
                        "equipo_visitante": equipo_visitante,
                        "marcador_visitante": marcador_visitante
                    })
                    print(f"Partido {i+1}: {equipo_local} {marcador_local} - {marcador_visitante} {equipo_visitante}")
            # El código no imprime nada si los datos no son válidos, simplemente los salta.
        except Exception as e:
            # Puedes usar 'pass' para no hacer nada o dejar un 'print' para depuración.
            print(f"Error en partido {i+1}: {str(e)}")
    
    # 6. Crear y limpiar el DataFrame de Pandas
    if resultados_partidos:
        df = pd.DataFrame(resultados_partidos)
        
        df['marcador_local'] = pd.to_numeric(df['marcador_local'], errors='coerce')
        df['marcador_visitante'] = pd.to_numeric(df['marcador_visitante'], errors='coerce')
        df = df.dropna()
        df = df.reset_index(drop=True)
        
        print("\n--- Vista previa del DataFrame limpio ---")
        print(df.head())
        print("------------------------------------------\n")
    else:
        print("\nNo se encontraron resultados para crear el DataFrame.")

except Exception as e:
    print(f"Error general: {str(e)}")
    print(f"URL final: {driver.current_url}")
    print(f"Título: {driver.title}")
    
    with open('debug_page.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print("HTML guardado en debug_page.html")

finally:
    driver.quit()