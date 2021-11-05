# climate_power_generation
El siguiente repositorio de código genera un dataset en csv que combina información de generación de energía a través de REE, climatológica a través de la AEMET y de consumo de un usuario por su comercializadora y tiene datos desde enero 2020 a septiembre 2021

# Contiene los siguientes ficheros:
API_Red_Electrica.py
Este código contiene el código para obtener información sobre la generación y demanda de energía extraído de la web de Red Eléctrica de España, separado por tipo de generación (hidráulico, eólico etc), consumo de energía, emisiones de CO2 etc.
Su clave primaria es la fecha y cada registro corresponde a 1 día desde el 1 de enero del 2020 al 30 de septiembre del 2021

webscraping_aemet.py
Este código genera llamadas sobre la web de la AEMET. Selecciona una estación en cada provincia de España y obtiene la información sobre la temperatura, precipitaciones y velocidad del viento.
La clave primaria es la fecha. Como en el caso anterior, cada registro corresponde a 1 día desde el 1 de enero del 2020 al 30 de septiembre del 2021.

webscraping_comercializa.py
Este código genera llamadas sobre la web i-DE de Iberdrola. Hace login en la web y mantiene la sesión abierta. A continuación realiza llamadas diarias y recoge la información del consumo durante las 24 horas del día.
La vlave primaria es la fecha. Como en los dos casos anteriores, cada registo contiene 1 día y va del 1 de enero del 2020 al 30 de septiembre del 2021.