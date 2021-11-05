# Imports
Import pandas as pd
Import numpy as np
import requests


def web_scraping_aemet(fecha_inicio, fecha_fin, api_key):
    """ Esta función recoge los datos de una fecha inicio a una fecha final de temperatura media, precipitación y
        velocidad del viento de una estación metereológica de las comunidades autónomas de la península

        Entrada:
            fecha_inicio: Marca el inicio de la petición
            fecha_fin: Marca el fin de la petición
            Api_key: Api de la AEMET (válida por 5 días

        Salida:
            Fecha: Fecha del día de recogida de datos (primary key)
            Para cada estación:
                Nombre: Nonmbre de la estación metereológica
                tmed: Temperatura media del día
                prec: Precipitaciones del día
                velmedia: Velocidad media del viento
            """

    # Defino las estaciones que voy a recorrer
    estaciones = {"Galicia": "1387",
                  "Aragón": "9898",
                  "Catalunya": "0076",
                  "Asturias": "1212E",
                  "Cantabria": "1111X",
                  "Pais Vasco": "1082",
                  "Navarra": "1002Y",
                  "La Rioja": "9170",
                  "Aragon": "9434",
                  "C.Leon": "2661",
                  "Madrid": "3195",
                  "Extremadura": "4452",
                  "C.La Mancha": "3260B",
                  "Valencia": "8416Y",
                  "Murcia": "7178I",
                  "Andalucia": "5783"}


    i = 0

    # Itero sobre las diferentes estaciones definidas para hacer llamadas por cada una de ella
    for estacion in estaciones:
        identificador = estaciones[estacion]
        print(identificador)

        # Esta url nos dará como respuesta otra url donde se encuentran los datos
        url = ("https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/" +
               fecha_inicio + "/fechafin/" + fecha_fin + "/estacion/" + identificador + "/")

        querystring = {"api_key": api_key}

        headers = {
            'cache-control': "no-cache"
        }

        # Lanzamos la primera llamada
        response = requests.request("GET", url, headers=headers, params=querystring)

        # Analizo la vuelta de la llamada
        soup = response.text
        json_object = json.loads(soup) # Formato diccionario
        url_datos = json_object["datos"] # Seleccionamos el campo datos que nos da la nueva url

        # Lanzamos la segunda llamada
        response_data = requests.request("GET", url_datos, headers=headers)
        json_datos = json.loads(response_data.text)

        # Generamos en formato json la información de vuelta para analizarlo
        df_aemet = pd.json_normalize(json_datos)

        # Selecciono sólo unas pocas variables ya que en función de la estación tenemos acceso a unos pocos datos
        df_seleccion = df_aemet[["fecha", "nombre", "tmed", "prec", "velmedia"]] # Seleccionamos las variables

        # A las variables les incorporamos el sufijo
        for column in df_seleccion.columns:
            if column != "fecha":
                new_column = column + "_" + identificador
                df_seleccion = df_seleccion.rename(columns={column: new_column})

        # Para la primera llamada generamos el dataframe completo
        if i == 0:
            df_aemet_agrupado = df_seleccion
        else: # Para sucesivas llamadas vamos haciendo el merge para añadir variables
            df_aemet_agrupado = df_aemet_agrupado.merge(df_seleccion, how='inner', on='fecha')

        i = i + 1
    return df_aemet_agrupado