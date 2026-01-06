import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import random
import mysql.connector as sql
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env antes de usarlas
load_dotenv()


#Creamos las funcines
class bot_WS:
    
    def __init__(self):
        
        
        #Inciamos los parametros
        self.ruta_fichero = os.path.join(os.path.dirname(__file__), "bot_ws.log")
        self.ruta_perfil = os.getenv("RUTA_PERFIL")
        self.ruta_driver = os.getenv("RUTA_DRIVER")
        #Seteamos los parametros del bot
        self.service = Service(self.ruta_driver)
        self.options = Options()
        self.options.add_argument(f"-profile")
        self.options.add_argument(self.ruta_perfil)
        self.driver = webdriver.Firefox(service=self.service,options=self.options)
        self.data_dict = list()
        
    

    def felicitarCumpleaños(self):
        #Cargamos los datos de los cumpleaños
        self.cargar_datos()
        
        if len(self.data_dict) == 0: 
            self.abrir_was(None)
            
        else: 
            for x in self.data_dict:
                self.escribirLog(f"Enviando mensaje a {x['nombre']} al numero {x['numero']}")
                self.enviar_mensaje(x["numero"], x["nombre"])
                time.sleep(5)
        
        self.driver.quit()
        self.escribirLog("Cerrando navegador")



        return
    def enviar_mensaje(self, numero, nombre):
        
        """
            Envia un mensaje a un numero de whatshap a traves de la web
            
            :param numero: Numero de telefono al que se enviara el mensaje
            :param nombre: Nombre de la persona a felicitar 

        """
        
    
        if self.abrir_was(numero) == 2: return 
        mensaje = self.generar_mensaje(nombre)
        
        #Primero esperamos a que carque el chat
        chat = WebDriverWait(self.driver,60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".x78zum5.x1cy8zhl.x1y332i5.xggjnk3.x1yc453h"))
        )
        #Localizamos la caja de mensaje
        cajas = WebDriverWait(self.driver, 60).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".x1hx0egp.x6ikm8r.x1odjw0f.x1k6rcq7.x6prxxf"))
        )
        
        caja = cajas[1]

    
        #Enviamos el mensaje
        self.escribirLog(f"Enviando mensaje {mensaje} a {nombre} al numero {numero}")
        actions = ActionChains(self.driver)
        actions.click(caja)
        actions.send_keys(mensaje)
        time.sleep(7)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        time.sleep(7)
        self.escribirLog(f"Mensaje enviado a {nombre} al numero {numero}")
        return


    def abrir_was(self, numero):
        """
            Abre la aplicacion de whatsapp web para enviar un mensaje o para mantener la sesion abierta
            :param numero: Numero al que se enviara el mensaje, en caso de que no haya coincidencias
        """
        if numero: 
            url = f"https://web.whatsapp.com/send?phone=+34{numero}"
            self.driver.get(url)
            self.escribirLog(f"Abriendo chat con el numero {numero}")
            return 1
        else: 
            url = "https://web.whatsapp.com"
            self.driver.get(url)
            self.escribirLog("Abriendo WhatsApp Web sin numero")
            time.sleep(20)
            return 2
    
    def cargar_datos(self):
        
        fecha = time.strftime("%d-%m") 
        self.escribirLog(f"Cargando datos para la fecha {fecha}")
   
        conn = sql.connect(
            host=os.getenv("HOST_WS"),
            user=os.getenv("USER_WS"),
            password=os.getenv("PASSWORD_WS"),
            database=os.getenv("DATABASE_WS")
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT nombre_bot, nombre, telefono FROM cumples WHERE fecha = %s",(fecha,))
        resultado = cursor.fetchall()
        cursor.close()
        conn.commit()
        
        
        if resultado is None: 
            self.escribirLog(f"No se encontraron resultados para la fecha {fecha}")
            return resultado
        
        
        
        for r in resultado:
            data = {
                "numero": r[2],
                "nombre": r[0] if r[0] else r[1]
            }
            self.data_dict.append(data)
        self.escribirLog("Datos cargados correctamente")
        return


    def generar_mensaje(self,nombre):
    
        frases = (  
            f"¡Feliz cumpleaños, {nombre}! Espero que tengas un buen día.", 
            f"¡Felicidades en tu día, {nombre}! Que lo pases genial.", 
            f"¡Que tengas un gran cumpleaños, {nombre}! Disfruta del día.", 
            f"¡Feliz cumple, {nombre}! Espero que te diviertas.", 
            f"¡Felicidades, {nombre}! Que tengas un día excelente.",               
            f"¡Feliz cumpleaños, {nombre}! Que sea un día tranquilo y agradable.", 
            f"¡Que tengas un buen cumpleaños, {nombre}! A disfrutar de la celebración.", 
            f"¡Feliz cumple, {nombre}! Que el día sea justo como te gusta.", 
            f"¡Felicidades en tu cumpleaños, {nombre}! Que pases un día relajado.", 
            f"¡Feliz cumpleaños, {nombre}! Espero que tengas un buen rato."
        )
        return frases[random.randint(0,len(frases) - 1)]
    
    def escribirLog(self, mensaje):
        with open(self.ruta_fichero, "a") as f:
            f.write(f"[{time.strftime('%d-%m-%Y %H:%M:%S')}] - {mensaje}\n")
        return
        
        