"""
Script para capturar screenshots reales del frontend usando Playwright
Instalar: pip install playwright
Luego: playwright install chromium
"""

import asyncio
from pathlib import Path
import sys

async def capturar_screenshots_playwright():
    """Captura screenshots usando Playwright"""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("Playwright no está instalado.")
        print("Instala con: pip install playwright")
        print("Luego ejecuta: playwright install chromium")
        return False
    
    base_url = "http://localhost:8000"
    demo_dir = Path(__file__).parent
    frames_dir = demo_dir / "frames_reales"
    frames_dir.mkdir(exist_ok=True)
    
    print("Iniciando captura de screenshots del frontend real...")
    print(f"URL base: {base_url}")
    
    async with async_playwright() as p:
        # Iniciar navegador
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        screenshots_capturados = []
        
        try:
            # 1. Página de Login
            print("\n1. Capturando página de login...")
            await page.goto(f"{base_url}/accounts/login/", wait_until='networkidle')
            await page.wait_for_timeout(2000)  # Esperar animaciones
            await page.screenshot(path=str(frames_dir / "01_login.png"), full_page=True)
            screenshots_capturados.append("01_login.png")
            print("   [OK] Login capturado")
            
            # 2. Hacer login
            print("\n2. Iniciando sesion...")
            await page.fill('input[name="username"]', 'admin')
            await page.fill('input[name="password"]', 'admin123')
            await page.click('button[type="submit"]')
            await page.wait_for_timeout(3000)  # Esperar navegación
            print("   [OK] Sesion iniciada")
            
            # 3. Dashboard
            print("\n3. Capturando dashboard...")
            await page.goto(f"{base_url}/", wait_until='networkidle')
            await page.wait_for_timeout(3000)  # Esperar gráficos
            await page.screenshot(path=str(frames_dir / "02_dashboard.png"), full_page=True)
            screenshots_capturados.append("02_dashboard.png")
            print("   [OK] Dashboard capturado")
            
            # 4. Clientes
            print("\n4. Capturando lista de clientes...")
            await page.goto(f"{base_url}/clientes/", wait_until='networkidle')
            await page.wait_for_timeout(2000)
            await page.screenshot(path=str(frames_dir / "03_clientes.png"), full_page=True)
            screenshots_capturados.append("03_clientes.png")
            print("   [OK] Clientes capturado")
            
            # 5. Equipos
            print("\n5. Capturando lista de equipos...")
            await page.goto(f"{base_url}/equipos/", wait_until='networkidle')
            await page.wait_for_timeout(2000)
            await page.screenshot(path=str(frames_dir / "04_equipos.png"), full_page=True)
            screenshots_capturados.append("04_equipos.png")
            print("   [OK] Equipos capturado")
            
            # 6. Tickets
            print("\n6. Capturando lista de tickets...")
            await page.goto(f"{base_url}/tickets/", wait_until='networkidle')
            await page.wait_for_timeout(2000)
            await page.screenshot(path=str(frames_dir / "05_tickets.png"), full_page=True)
            screenshots_capturados.append("05_tickets.png")
            print("   [OK] Tickets capturado")
            
            # 7. Inventario
            print("\n7. Capturando inventario...")
            await page.goto(f"{base_url}/inventario/repuestos/", wait_until='networkidle')
            await page.wait_for_timeout(2000)
            await page.screenshot(path=str(frames_dir / "06_inventario.png"), full_page=True)
            screenshots_capturados.append("06_inventario.png")
            print("   [OK] Inventario capturado")
            
            # 8. Proveedores
            print("\n8. Capturando proveedores...")
            await page.goto(f"{base_url}/proveedores/", wait_until='networkidle')
            await page.wait_for_timeout(2000)
            await page.screenshot(path=str(frames_dir / "07_proveedores.png"), full_page=True)
            screenshots_capturados.append("07_proveedores.png")
            print("   [OK] Proveedores capturado")
            
            # 9. Facturación
            print("\n9. Capturando facturación...")
            await page.goto(f"{base_url}/facturacion/", wait_until='networkidle')
            await page.wait_for_timeout(2000)
            await page.screenshot(path=str(frames_dir / "08_facturacion.png"), full_page=True)
            screenshots_capturados.append("08_facturacion.png")
            print("   [OK] Facturacion capturado")
            
            # 10. Chatbot IA
            print("\n10. Capturando chatbot IA...")
            await page.goto(f"{base_url}/ia/chatbot/", wait_until='networkidle')
            await page.wait_for_timeout(2000)
            await page.screenshot(path=str(frames_dir / "09_chatbot.png"), full_page=True)
            screenshots_capturados.append("09_chatbot.png")
            print("   [OK] Chatbot capturado")
            
        except Exception as e:
            print(f"\nError durante la captura: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            await browser.close()
    
    print(f"\n{'='*50}")
    print(f"Captura completada: {len(screenshots_capturados)} screenshots")
    print(f"Ubicación: {frames_dir}")
    print(f"{'='*50}")
    
    return len(screenshots_capturados) > 0

if __name__ == "__main__":
    try:
        resultado = asyncio.run(capturar_screenshots_playwright())
        if resultado:
            print("\n[OK] Screenshots capturados exitosamente")
            print("Ahora ejecuta: python crear_demo_frontend_real.py")
        else:
            print("\n[ERROR] No se pudieron capturar los screenshots")
    except KeyboardInterrupt:
        print("\n\nCaptura cancelada por el usuario")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
