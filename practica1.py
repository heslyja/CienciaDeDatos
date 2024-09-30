"""
Alumna: Hesly Janeth Acosta Chavez
Grupo: 382
"""
# Librerias
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

# Creo una funcion para poder buscar en la pag Amazon
def busquedaAutomatizada(palabra, pags, img):
    # Configuro el navegador Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # Indico que pagina se abrira
    driver.get("https://www.amazon.com.mx/")
    # Para maximizar la ventana del navegador
    driver.maximize_window()

    # Agregamos el suficiente tiempo para poder resolver de manera manual el captcha que esta al abrir la pagina
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
    # Se introducira lo que busquemos, la cual esta definida casi al final del codigo
    driver.find_element(By.ID, "twotabsearchtextbox").send_keys(palabra + Keys.RETURN)
    # Recorre las paginas que se quieran buscar, tambien definidas mas abajo

    #Creo un contador para las paginas
    current_page = 0
    # Mientras el contador sea menor que el total de pags indicadas se seguira repitiendo
    while current_page < pags:
        # Espera a que se carguen los resultados en la pagina
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".s-main-slot")))

        # Si la pagina actual es menor que el numero de imagenes, toma una captura
        if current_page < img:
            driver.save_screenshot(f'Cap {current_page + 1}.png')

        try:
            # Se pulsara el boton sig cuando este disponible
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.s-pagination-next"))
            )
            # Se pulsara el boton sig e ira a la pag sig
            next_button.click()
            # Aumenta el contador de pags
            current_page += 1
            # Damos tiempo para que cargue la pagina siguiente
            time.sleep(2)
        except:
            # Si ya no hay paginas se sale del bucle
            break
    # Esto es para cerrar el navegador cuando ya ejecuto todo el script
    driver.quit()
# Indicamos los parametros deseados, palabra, pagina y capturas
busquedaAutomatizada("monitor gamer", 3, 3)