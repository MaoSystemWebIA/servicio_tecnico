"""
Script para capturar screenshots reales del frontend de la aplicación
y crear un video demo más realista
"""

import time
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def setup_driver():
    """Configura el driver de Selenium"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Ejecutar sin ventana
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-gpu')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Error al configurar Chrome: {e}")
        print("Intentando con Firefox...")
        try:
            from selenium.webdriver.firefox.options import Options as FirefoxOptions
            firefox_options = FirefoxOptions()
            firefox_options.add_argument('--headless')
            driver = webdriver.Firefox(options=firefox_options)
            return driver
        except:
            print("No se encontró ningún navegador compatible")
            return None

def capturar_screenshot(driver, url, nombre_archivo, wait_element=None):
    """Captura un screenshot de una URL"""
    try:
        print(f"Capturando: {url}")
        driver.get(url)
        time.sleep(2)  # Esperar a que cargue
        
        # Esperar elemento específico si se proporciona
        if wait_element:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, wait_element))
                )
            except TimeoutException:
                print(f"  Advertencia: No se encontró el elemento {wait_element}")
        
        time.sleep(1)  # Esperar adicional para animaciones
        
        # Capturar screenshot
        screenshot_path = Path(__file__).parent / "frames_reales" / nombre_archivo
        screenshot_path.parent.mkdir(exist_ok=True)
        driver.save_screenshot(str(screenshot_path))
        print(f"  Guardado: {screenshot_path}")
        return True
    except Exception as e:
        print(f"  Error al capturar {url}: {e}")
        return False

def main():
    """Función principal"""
    base_url = "http://localhost:8000"
    demo_dir = Path(__file__).parent
    frames_dir = demo_dir / "frames_reales"
    frames_dir.mkdir(exist_ok=True)
    
    print("Iniciando captura de screenshots del frontend real...")
    print(f"URL base: {base_url}")
    
    driver = setup_driver()
    if not driver:
        print("\nNo se pudo configurar el navegador.")
        print("Instala Chrome o Firefox, o usa el método alternativo con herramientas del navegador.")
        return
    
    try:
        screenshots = []
        
        # 1. Página de login
        if capturar_screenshot(driver, f"{base_url}/accounts/login/", "01_login.png", "form"):
            screenshots.append("01_login.png")
        
        # 2. Login (necesitamos hacer login primero)
        driver.get(f"{base_url}/accounts/login/")
        time.sleep(2)
        try:
            username_field = driver.find_element(By.NAME, "username")
            password_field = driver.find_element(By.NAME, "password")
            username_field.send_keys("admin")
            password_field.send_keys("admin123")
            login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            time.sleep(3)  # Esperar a que cargue el dashboard
        except Exception as e:
            print(f"Error al hacer login: {e}")
            print("Continuando sin login...")
        
        # 3. Dashboard
        if capturar_screenshot(driver, f"{base_url}/", "02_dashboard.png", "body"):
            screenshots.append("02_dashboard.png")
        
        # 4. Lista de Clientes
        if capturar_screenshot(driver, f"{base_url}/clientes/", "03_clientes.png", "body"):
            screenshots.append("03_clientes.png")
        
        # 5. Lista de Equipos
        if capturar_screenshot(driver, f"{base_url}/equipos/", "04_equipos.png", "body"):
            screenshots.append("04_equipos.png")
        
        # 6. Lista de Tickets
        if capturar_screenshot(driver, f"{base_url}/tickets/", "05_tickets.png", "body"):
            screenshots.append("05_tickets.png")
        
        # 7. Inventario
        if capturar_screenshot(driver, f"{base_url}/inventario/repuestos/", "06_inventario.png", "body"):
            screenshots.append("06_inventario.png")
        
        # 8. Proveedores
        if capturar_screenshot(driver, f"{base_url}/proveedores/", "07_proveedores.png", "body"):
            screenshots.append("07_proveedores.png")
        
        # 9. Facturación
        if capturar_screenshot(driver, f"{base_url}/facturacion/", "08_facturacion.png", "body"):
            screenshots.append("08_facturacion.png")
        
        # 10. Chatbot IA
        if capturar_screenshot(driver, f"{base_url}/ia/chatbot/", "09_chatbot.png", "body"):
            screenshots.append("09_chatbot.png")
        
        print(f"\nCapturadas {len(screenshots)} screenshots exitosamente")
        print(f"Ubicación: {frames_dir}")
        
    finally:
        driver.quit()
        print("\nNavegador cerrado")

if __name__ == "__main__":
    main()
