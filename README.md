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

mi_consumo.csv
Como el objetivo es no impedir el funcionamiento de i-DE, tras la implementación del código, se extrajo la información relacionada con el consumo diario hora a hora en un csv. A partir de entonces y a falta de productivizarlo se leerá el csv.

main.py
Este es el fichero principal del código. Llama a los tres códigos y los unifica en una única base de datos. Los tres datasets se unen mediante la clave primaria de fecha por lo que se genera el fichero final dataset_completo.csv que será el que se publique.

dataset_completo.csv
Este fichero recoge la unificación de las tres bases de datos (AEMET, REE e i-DE). La clave primaria es la fecha y cada registro recoge 1 día entre el 1 de enero del 2020 y el 31 de septiembre del 2021. Es el que se subirá a Zenodo.

El csv final se ha subido a la web Zenodo:
DOI: 10.5281/zenodo.5601489
URL: https://zenodo.org/record/5601489#.YXhDy9pByUk
