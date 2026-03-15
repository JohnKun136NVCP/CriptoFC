# SQL Injection
La inyección SQL (SQLi) es una vulnerabilidad de seguridad web donde un atacante inserta comandos SQL maliciosos en los campos de entrada de una aplicación (formularios, URLs), logrando manipular la base de datos subyacente sin autorización. Esto permite leer, modificar o eliminar datos sensibles y comprometer la seguridad del servidor. 

Para este último ejercicio va ser de manera muy práctica, para ello debe leer los siguientes requerimientos. 

- Instale un entorno virtual
- Corra el entorno virtual
- Use el comando ```pip install Flask```
- Descargue las carpetas sin romper el orden por favor.

Una vez hecho esto, solamente corra el programa ```python3 app.py```, no hay nada de que preocuparse. Solamente correrá un servició de Back-End de manera para desplegar una página.

- Vaya a la dirección local que le indica y abrala con su navegador. Verá un sitio web (medio hacer)

- Invesgue las sentencias lógicas para el uso de SQL Injection

- Intente probar hasta que lo deje loguear y después aparezca cierta información en partícular.

- Dentro de la información que aparece, hay un texto muy largo, copie ese texto y vaya a la página https://gchq.github.io/CyberChef/ 

- Del lado derecho verá un apartado donde dice **Favorites**, arrastre la opción donde dice *From Base64* al apartado *recipe*.
- Una vez hecho esto, copie el texto largo y peguelo a donde dice *input* en la página. Después de click en **BAKE!** sino aparece nada, sino saldrá el mensaje oculto.
