import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

#Creamos las funcines
def generarURL(numero):
    url = f"https://web.whatsapp.com/send?phone=+34{numero}"
    return url

def EnviarMensaje(numero,mensaje):
    #Creamos las variables que tendran los datos
    ruta_perfil = '/ruta/perfil/firefox'
    ruta_driver = '/ruta/driver/geckodriver'


    #Inciamos los parametres
    service = Service(ruta_driver)
    options = Options()
    options.add_argument(f"-profile")
    options.add_argument(ruta_perfil)
    driver = webdriver.Firefox(service=service,options=options)

    #Programa principal
    url = generarURL(numero)
    driver.get(url)
    #Dejamos una pequeÃ±a pausa para que carga was
    time.sleep(20)
    
    caja = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')

   
    #Enviamos el mensaje
    actions = ActionChains(driver)
    actions.click(caja)
    actions.send_keys(mensaje)
    actions.send_keys(Keys.ENTER)
    actions.perform()

    time.sleep(5)
    driver.quit()
    return


def abrirWas():
    #Creamos las variables que tendran los datos
    ruta_perfil = '/ruta/perfil/firefox'
    ruta_driver = '/ruta/driver/geckodriver'
    url = "https://web.whatsapp.com"

    #Inciamos los parametres
    service = Service(ruta_driver)
    options = Options()
    options.add_argument(f"-profile")
    options.add_argument(ruta_perfil)
    driver = webdriver.Firefox(service=service,options=options)

    #Programa principal
    driver.get(url)
    time.sleep(20)
    driver.quit()
    return