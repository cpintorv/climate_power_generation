# imports
import pandas as pd
import numpy as np
import requests


def web_scraping_iberdrola(user,passwd, fecha_inicio, fecha_fin):
    """'La siguiente función recoge el consumo diario de la fecha de inicio a la de fin
        pasándole el usuario y la contraseña

        Entrada:
            user: usuario en la web IDE de iberdrola
            passwd: contraseña de la web
            fecha_inicio: Fecha de inicio de la recogida de datos
            fecha_fin: Fecha fin de la recogida de datos

        Devuelve:
            Fecha: Cada una de las fechas de inicio a fin de la llamada
            1-24: Consumo durante las 24 horas
        """
    # Establece conexión y recibe el ok (200) o KO
    session_requests = requests.session()

    # Declaro la cabecera de la llamada seleccionada de una llamada monitorizada
    headers = {
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'dispositivo': 'desktop',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json, text/plain, */*',
        'Referer': '',
        'sec-ch-ua-platform': '"Windows"',
        'AppVersion': 'v2',
    }

    # Datos de usuario y password para logarme en el Iberdrola
    data = '["'+user+'","'+passwd+'",null,"Windows 10","PC","Chrome 94.0.4606.81","0","","n"]'

    # Lllamada para logarse
    response = session_requests.post('https://www.i-de.es/consumidores/rest/loginNew/login', headers=headers, data=data)

    # Nueva cabecera
    headers = {
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'dispositivo': 'desktop',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json, text/plain, */*',
        'Referer': '',
        'sec-ch-ua-platform': '"Windows"',
        'AppVersion': 'v2',
    }

    # Imprimo el estado que en el caso de ser 200 será OK
    print(response.status_code)

    # La fecha de inicio y fin la recojo de los parámetros de entrada
    anyo_inicio = fecha_inicio[0]
    mes_inicio = fecha_inicio[1]
    dia_inicio = fecha_inicio[2]
    anyo_fin = fecha_fin[0]
    mes_fin = fecha_fin[1]
    dia_fin = fecha_fin[2]
    start_date = datetime. date(anyo_inicio, mes_inicio, dia_inicio)
    end_date = datetime. date(anyo_fin, mes_fin, dia_fin)
    delta = datetime. timedelta(days=1)

    # Bucle iterativo de llamadas a Iberdrola
    i = 0
    while start_date <= end_date:
        year = start_date.year
        month = start_date.month
        day = start_date.day
        fecha_spanish = str('%02d' %day)+'-'+str('%02d' %month) + '-' +str(year)
        fecha_columna = str(year) +'-'+str('%02d' %month) + '-' + str('%02d' %day)
        url='https://www.i-de.es/consumidores/rest/consumoNew/obtenerDatosConsumoDH/'+fecha_spanish+'/'+fecha_spanish+'/horas/'
        response = session_requests.get(url) #Llamada a iberdrola por cada día para recoger el consumo por horas
        soup = response.text # Me quedo con el resultado
        horas = ['h1','h2','h3','h4','h5','h6','h7','h8','h9','h10','h11','h12',
                 'h13','h14','h15','h16','h17','h18','h19','h20','h21','h22','h23','h24','fecha']
        datos = soup[1:-1] # Lo dejo en formato diccionario
        json_datos = json.loads(datos) # Lo convierto en un diccionario
        json_datos = list(json_datos["valores"]) # Hago una lista con los 24 valores por horas
        if len(json_datos)==24: # Sólo selecciono el día si tiene 24 registros (hay casos con 23)
            json_datos.append(fecha_columna) # Incorporaré a las columnas la fecha que será el primary key
            valor_array=np.array([json_datos],dtype=object) # Los datos los paso a un array
            if i==0: # El primer día genero el dataframe
                df_consumo = pd.DataFrame(valor_array,columns=horas)
            else: # El resto voy añadiendo registros
                df_tmp = pd.DataFrame(valor_array,columns=horas)
                df_consumo = df_consumo.append(df_tmp)
            i+=1
            print(fecha_spanish)
            time.sleep(3) # Llamo cada 3 segundos acordado con Iberdrola tras la revocación
        start_date += delta # Sumo un día
    return df_consumo