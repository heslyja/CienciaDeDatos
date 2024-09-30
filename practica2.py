"""
Alumna: Hesly Janeth Acosta Chavez
Grupo: 382
Meta 2.4 Implementar proceso de Web Scraping usando Beautiful Soup
"""

# Librerias
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

# Creo una funcion para poder buscar en la pag Amazon
def amazon_scraper(busqueda, pags):
    # Configura el navegador Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # Indico que pagina se abrira
    driver.get("https://www.amazon.com.mx/")
    # Para maximizar la ventana del navegador
    driver.maximize_window()
    # Se introducira lo que busquemos, la cual esta definida casi al final del codigo
    driver.find_element(By.ID, "twotabsearchtextbox").send_keys(busqueda + Keys.RETURN)

    #  Lista para almacenar los datos de los productos
    productos = []
    pags_scrapeadas = 0

    while pags_scrapeadas < pags:
        # Espera a que se carguen los resultados
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".s-main-slot")))
        # Parsea el contenido de la pagina
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # Encuentra todos los productos en la pagina
        items = soup.find_all('div', {'data-component-type': 's-search-result'})

        # Extrae la informacion de cada producto
        for item in items:
            nombre = item.find('span', {'class': 'a-size-base-plus a-color-base a-text-normal'})
            precio = item.find('span', {'class': 'a-price-whole'})
            fecha_entrega = item.find('span', {'class': 'a-color-base a-text-bold'})
            rating = item.find('span', {'class': 'a-icon-alt'})

            # Para manejar datos faltantes
            if nombre:
                nombre = nombre.text
            else:
                nombre = 'Sin nombre'

            if precio:
                precio = precio.text
            else:
                precio = '0'

            if fecha_entrega:
                fecha_entrega = fecha_entrega.text
            else:
                fecha_entrega = 'Sin fecha de entrega'

            if rating:
                rating = rating.text.split()[0]
            else:
                rating = '0'

            # Agrega los datos del producto a la lista
            productos.append({
                'Nombre': nombre,
                'Precio': precio,
                'Fecha de entrega': fecha_entrega,
                'Rating': rating
            })

        # Aumenta el contador cada que se scrapea una pagina
        pags_scrapeadas += 1

        # Si el numero de paginas scrapeadas actual es menor que el numero de paginas, pasa a la siguiente pagina
        if pags_scrapeadas < pags:
            try:
                # Se pulsara el boton sig cuando este disponible
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.s-pagination-next"))
                )
                # Se pulsara el boton sig
                next_button.click()
                # Damos tiempo para que cargue la pagina siguiente
                time.sleep(2)
            except:
                break

    # Esto es para cerrar el navegador
    driver.quit()

    # Crea el DataFrame directamente de la lista
    df = pd.DataFrame(productos)
    # Guarda en CSV
    df.to_csv(f'productos_amazon.csv', index=False, encoding='utf-8-sig')

    return df

# Indicamos los parametros deseados, palabra y paginas
resultados = amazon_scraper("monitor gamer", 3)
print(resultados)


