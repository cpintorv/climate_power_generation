# Import libraries
import datetime
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
import calendar
from dateutil.relativedelta import relativedelta
import numpy as np
from collections import OrderedDict

# Function API de red electrica
def iteracion(endpoint, start_date, end_date, sufijo):
    '''
    Función que extrae la información de la API de Red eléctrica para unas fechas en concreto
    :param start_date: Fecha de inicio desde la cual se desea obtener la información
    :param end_date: Fecha de final para la cual se desea obtener la información
    :param sufijo: Sufijo para añadir en el nombre de las variables, en función del endpoint que se
    está consultando
    :param endpoint: Endpoint del cual se desea obtener los datos
    :return: Devuelve un dataframe que contiene un registro para cada uno de los días con toda
    la información
    '''

    # En la llamada a la API hay un máximo de 366 días, por lo tanto se hace una llamada mes a mes

    strweb = 'https://apidatos.ree.es/es/datos' + endpoint+'?start_date=' + start_date + \
             'T00:00&end_date=' + end_date + 'T23:59&time_trunc=day'
    # Se llama a la API
    page = requests.get(strweb)
    soup = BeautifulSoup(page.content, "html.parser")
    # Se convierte en un objeto JSON
    site_json = json.loads(soup.text)
    # Se calcula cuantos tipos de energía hay
    tipos = site_json['included']
    len_origen = len(tipos)

    # Inicializo las listas
    tipo_list = []
    tipo_sub_list = []
    values = []
    dates = []
    dfs = []

    # En función del endpoint que se esté consultando, la estructura del JSON es diferente
    if endpoint == '/balance/balance-electrico':
        for k in range(len_origen): # Se itera sobre las diferentes valores
            tipo = tipos[k]['type']
            len_att = len(site_json['included'][k]['attributes']['content'])
            for n in range(len_att):
                tipo_sub = site_json['included'][k]['attributes']['content'][n]['type']
                len_values = len(site_json['included'][k]['attributes']['content'][n]['attributes']['values'])
                for p in range(len_values):
                    value = site_json['included'][k]['attributes']['content'][n]['attributes']['values'][p]['value']
                    date = site_json['included'][k]['attributes']['content'][n]['attributes']['values'][p]['datetime']
                    # Hay muy pocos días que existe información de Fuel + Gas, por lo tanto se hace un control para
                    # no cargarlo, la aportación es mínima
                    if(tipo_sub != 'Fuel + Gas'):
                        tipo_list.append(tipo)
                        tipo_sub_list.append(tipo_sub)
                        values.append(value)
                        dates.append(date[0:10])
                # En septiembre del 2021 no hay datos para el día 13 de hidroeólica, se ajusta
                if tipo_sub == 'Hidroeólica' and start_date == '2021-09-01':
                    values.insert(132, 0.0)
                    dates.insert(132, '2021-09-13')
                    print(dates)

    if endpoint == '/generacion/estructura-generacion':
        for k in range(len_origen):
            tipo_sub = tipos[k]['type']
            len_att = len(site_json['included'][k]['attributes']['values'])
            for n in range(len_att):
                tipo = site_json['included'][k]['attributes']['type']
                value = site_json['included'][k]['attributes']['values'][n]['value']
                date = site_json['included'][k]['attributes']['values'][n]['datetime']
                if tipo_sub != 'Fuel + Gas':
                    tipo_list.append(tipo)
                    tipo_sub_list.append(tipo_sub)
                    values.append(value)
                    dates.append(date[0:10])
            # En septiembre del 2021 no hay datos para el día 13 de hidroeólica, se ajusta
            if tipo_sub == 'Hidroeólica' and start_date == '2021-09-01':
                values.insert(252,0.0)
                dates.insert(252,'2021-09-13')

    # Este fragmento de código es común para los dos endpoints.
    # Se crea un dataframe para cada uno de los días y se unen
    dias = int((len(values))/(len(set(tipo_sub_list))))
    cabecera = list(OrderedDict.fromkeys(tipo_sub_list))

    cabecera = [element + ' ' + sufijo for element in cabecera]
    cabecera_f = ['Fecha'] + cabecera
    val_add = np.arange(0, len(cabecera)*dias, dias).tolist()
    for q in range(dias):
        print('Ejecutando dia: ' + str(q))
        valores_final = []
        if q != 0:
            multiplied_list = [element + q for element in val_add]
        else:
            multiplied_list = val_add
        for m in range(len(values)):
            if m in multiplied_list:
                valores_final.append(values[m])
        valores_f = [dates[q]] + valores_final
        df = pd.DataFrame([valores_f], columns=cabecera_f)
        dfs.append(df)
    df_final = pd.concat(dfs)
    return df_final

# Imoprt extract data
def extract_api_re(endpoint, start_date, end_date, sufijo):
    '''
    Esta función calcula el número de veces que hay que llamar a la función interación, en función de los meses
    que haya entre start_date y end_date
    :param endpoint: Endpoint que se quiere consultar para extraer los datos
    :param start_date: Fecha inicio para la extracción
    :param end_date: Fecha final para la extracción
    :param sufijo: Sufijo para identificar el nombre de las variables de salida
    :return: devuelve un único dataframe con todos los datos
    '''
    # Cálculo del número de meses
    start_date_c = datetime.datetime(int(start_date[0:4]), int(start_date[5:7]), int(start_date[8:10]))
    end_date_c = datetime.datetime(int(end_date[0:4]), int(end_date[5:7]), int(end_date[8:10]))
    num_months = (end_date_c.year - start_date_c.year) * 12 + (end_date_c.month - start_date_c.month)
    dataframes = []
    # Se realiza una extracción por mes
    for k in range(num_months + 1):
        start_date_it = start_date_c + relativedelta(months=k)
        d_end = start_date_it.replace(day=calendar.monthrange(start_date_it.year, start_date_it.month)[1])
        d_start = start_date_it.replace(day=1)
        print('Extrayendo desde ' + str(d_start.date()) + ' hasta ' + str(d_end.date()))
        df = iteracion(endpoint, str(d_start.date()), str(d_end.date()), sufijo)
        dataframes.append(df)

    total_data = pd.concat(dataframes)
    return total_data
