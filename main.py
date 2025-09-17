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
    
    # 5. Procesar cada partido
    for i, partido in enumerate(partidos):
        try:
            # Buscar equipos con la clase específica que mencionaste
            equipos = partido.find_elements(By.CSS_SELECTOR, ".ScoreCell__TeamName.ScoreCell__TeamName--shortDisplayName.db")
            
            # Buscar marcadores
            marcadores = partido.find_elements(By.CSS_SELECTOR, ".ScoreCell__Score")
            
            if len(equipos) >= 2 and len(marcadores) >= 2:
                equipo_local = equipos[0].text
                equipo_visitante = equipos[1].text
                marcador_local = marcadores[0].text
                marcador_visitante = marcadores[1].text
                
                print(f"Partido {i+1}: {equipo_local} {marcador_local} - {marcador_visitante} {equipo_visitante}")
            else:
                print(f"Partido {i+1}: No se encontraron todos los datos necesarios")
                
        except Exception as e:
            print(f"Error en partido {i+1}: {str(e)}")
    
    # 6. Opcional: También buscar información adicional como ligas o tiempos
    try:
        ligas = driver.find_elements(By.CSS_SELECTOR, ".Card__Header__Title")
        for i, liga in enumerate(ligas):
            print(f"Liga {i+1}: {liga.text}")
    except:
        print("No se pudieron obtener las ligas")

except Exception as e:
    print(f"Error general: {str(e)}")
    print(f"URL final: {driver.current_url}")
    print(f"Título: {driver.title}")
    
    # Guardar HTML para debug
    with open('debug_page.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print("HTML guardado en debug_page.html")

finally:
    driver.quit()