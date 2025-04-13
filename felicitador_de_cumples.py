import time
import random
import pandas as pd
import enviarMensajes as eM



#Leemos los datos del fichero donde estan los cumpleaños
def cargar_datos():
   
    df = pd.read_csv("ruta/archivo/csv")   
    data_dict = dict()
    for nombre,fecha,telefono in zip(df["nombre"],df["fecha(d-m)"],df["telefono"]):
        data_dict[nombre] = (fecha,telefono)
        
    return data_dict
    
#Esta funcion nos devuelve un mensaje aleatorio, se pueden cambiar para mayor personalizacion    
def tipo_mensaje(nombre):
    
    frases = (  f"¡Feliz cumpleaños, {nombre}! Espero que tengas un buen día.", 
                f"¡Felicidades en tu día, {nombre}! Que lo pases genial.", 
                f"¡Que tengas un gran cumpleaños, {nombre}! Disfruta del día.", 
                f"¡Feliz cumple, {nombre}! Espero que te diviertas.", 
                f"¡Felicidades, {nombre}! Que tengas un día excelente.",               
                f"¡Feliz cumpleaños, {nombre}! Que sea un día tranquilo y agradable.", 
                f"¡Que tengas un buen cumpleaños, {nombre}! A disfrutar de la celebración.", 
                f"¡Feliz cumple, {nombre}! Que el día sea justo como te gusta.", 
                f"¡Felicidades en tu cumpleaños, {nombre}! Que pases un día relajado.", 
                f"¡Feliz cumpleaños, {nombre}! Espero que tengas un buen rato.")
    
    numero_frase = random.randint(0,len(frases) - 1)

    return frases[numero_frase]

#Ejecutamos el programa principal
def mandar_mensaje(nombre,telefono):
    eM.EnviarMensaje(telefono,tipo_mensaje(nombre))
    return
    
    

    
#Buscamos coincidencias    
def programa_principal():
    
    fecha = time.strftime("%d-%m")
    coincidencia = False
    for x in cumples.items():
        
        if x[1][0] == fecha: 
            mandar_mensaje(x[0],x[1][1])
            coincidencia = True
            break
    #Si no hay coincidencias, abrimos whatsapp igual para que no
    # se cierre la sesion
    if (coincidencia == False):
        eM.abrirWas()
        
    return

            
cumples = cargar_datos()
programa_principal()       

