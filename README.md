Bot WhatsApp con Selenium
==========================

Automatiza el envio de mensajes de WhatsApp Web (por ejemplo, felicitaciones de cumpleanos) usando Selenium y Firefox. Lee contactos y fechas desde MySQL, mantiene la sesion con un perfil local de Firefox y registra la actividad en un log.

Contenido
---------
- Caracteristicas clave
- Requisitos previos
- Instalacion
- Configuracion (.env y base de datos)
- Uso rapido
- Flujo interno
- Resolucion de problemas

Caracteristicas clave
---------------------
- Envio automatico de mensajes personalizados a partir de una lista en MySQL.
- Reutilizacion de sesion de WhatsApp Web mediante un perfil local de Firefox.
- Esperas explicitas (WebDriverWait) para mejorar la robustez frente a cambios de carga.
- Registro en archivo `bot_ws.log` con marcas de tiempo.

Requisitos previos
------------------
- Python 3.10+.
- Firefox instalado.
- Geckodriver compatible con tu version de Firefox y disponible en disco.
- Una sesion activa de WhatsApp Web asociada al perfil de Firefox que usaras.
- Acceso a una base de datos MySQL con la tabla `cumples` (ver esquema abajo).

Instalacion
-----------
1) Crea y activa un entorno virtual (opcional pero recomendado).
2) Instala dependencias:
	```bash
	pip install -r requirements.txt
	```

Configuracion
-------------
1) Variables de entorno (`.env` en la raiz):
	```env
	HOST_WS=localhost
	USER_WS=usuario
	PASSWORD_WS=contraseña
	DATABASE_WS=nombre_bd
	```

2) Perfil de Firefox y geckodriver:
	- Genera o identifica un perfil de Firefox que ya tenga iniciada sesion en WhatsApp Web.
	- Guarda la ruta del perfil y de `geckodriver.exe`; se pasan al inicializar el bot.

3) Esquema minimo de base de datos MySQL (tabla `cumples`):
	```sql
	CREATE TABLE cumples (
	  id INT AUTO_INCREMENT PRIMARY KEY,
	  fecha VARCHAR(5) NOT NULL,        -- formato DD-MM
	  nombre_bot VARCHAR(100) NULL,
	  nombre VARCHAR(100) NOT NULL,
	  telefono VARCHAR(20) NOT NULL
	);
	-- Ejemplo de insercion: 05-01 corresponde al 5 de enero
	INSERT INTO cumples (fecha, nombre_bot, nombre, telefono)
	VALUES ('05-01', 'Juan', 'Juan Perez', '600123123');
	```

Uso rapido
----------
Ejemplo con la clase principal definida en `main.py`:
```python
from main import bot_WS

if __name__ == "__main__":
	 perfil_firefox = r"C:\ruta\perfil\firefox"
	 ruta_geckodriver = r"C:\ruta\geckodriver.exe"

	 bot = bot_WS(perfil_firefox, ruta_geckodriver)
	 bot.felicitarCumpleanos()
```

Notas importantes:
- `felicitarCumpleanos()` carga los registros de `cumples` para la fecha actual (DD-MM) y envia un mensaje aleatorio de la lista interna.
- El log se escribe en `bot_ws.log` junto al codigo.
- El perfil de Firefox debe permanecer valido; si la sesion expira, abre WhatsApp Web manualmente con ese perfil y reescanea el QR.

Flujo interno
-------------
- `cargar_datos()`: obtiene los contactos de la tabla `cumples` segun la fecha actual.
- `abrir_was()`: abre WhatsApp Web (con o sin numero). Devuelve 1 si abre un chat especifico, 2 si solo mantiene la sesion.
- `enviar_mensaje()`: espera a que cargue el chat, ubica la caja de texto y envia el mensaje generado.
- `generar_mensaje()`: elige una frase de felicitacion al azar.

Resolucion de problemas
-----------------------
- El navegador se cierra antes de tiempo: aumenta los `sleep` o revisa la estabilidad de tu conexion.
- No encuentra la caja de mensaje: verifica que los selectores CSS no hayan cambiado en WhatsApp Web; ajustalos en `enviar_mensaje` si es necesario.
- Sesion expirada: abre manualmente WhatsApp Web con el perfil indicado y vuelve a escanear el QR.
- Problemas con MySQL: confirma credenciales y que el formato de `fecha` en la tabla sea `DD-MM`.

