from webscraping_comercializa import web_scraping_iberdrola
from webscraping_aemet import  web_scraping_aemet
import pandas as pd
from API_Red_Electrica import extract_api_re

# 1- LLAMADA A IBERDROLA Y RECOGIDA DE DATOS DE CONSUMO
# Llamada a la web de iberdrola y recogida de datos
#df_miconsumo = web_scraping_iberdrola("cpintorvillar@gmail.com","Heroes30",[2020, 1, 1],[2021, 9, 30])
#df_miconsumo.to_csv(r'C:\Users\c_pin\PycharmProjects\pythonProject\mi_consumo.csv', index=False)
# En lugar del original usaré éste para que no me revoquen en Iberdrola
df_miconsumo = pd.read_csv('C:/Users/c_pin/PycharmProjects/pythonProject/mi_consumo.csv', sep = ',')
print(df_miconsumo)

# 2- LLAMADA A AEMET Y RECOGIDA DATOS CLIMÁTICOS
# Llamada a la web de la aemet y recogida de datos
fecha_inicio = "2020-01-01T00:00:00UTC"
fecha_fin = "2021-10-01T00:00:00UTC"
api_key="eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjcGludG9ydmlsbGFyQGdtYWlsLmNvbSIsImp0aSI6ImY5NTIxMTI1LTIyY2MtNDA1NS1iMTEzLTJmM2Q1OTY2ZWU2MSIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNjM0NzM2Mzg3LCJ1c2VySWQiOiJmOTUyMTEyNS0yMmNjLTQwNTUtYjExMy0yZjNkNTk2NmVlNjEiLCJyb2xlIjoiIn0.5CoYoH1ExA5thNHvX7PR9NC6lMMkzcu4mN_4zglzXW0"
df_aemet =web_scraping_aemet(fecha_inicio,fecha_fin,api_key)
print(df_aemet)

# 3- LLAMADA A RED ELÉCTRICA Y RECOGIDOS DATOS DE GENERACIÓN
# Asignación de fechas inicio y final
start_date = '2020-01-01'
end_date = '2021-09-30'
# Llamada a la función extract_api_re para los endpoints de generacion y balance
df_generacion = extract_api_re('/generacion/estructura-generacion', start_date, end_date, 'Gen')
df_balance = extract_api_re('/balance/balance-electrico', start_date, end_date, 'Bal')
# Join de los resultados por la variable Fecha y exportación del CSV
result = pd.merge(df_balance, df_generacion, on='Fecha')
result = result.rename(columns={'Fecha': 'fecha'})
#result.to_csv(r'C:\Users\enriq\Desktop\Kike\UOC\SI - Tipología y ciclo de los datos\PRA1\output_file.csv', index=False)
print(result)

# 4- Unimos los tres dataframes en uno sólo y lo exportamos a csv
df_ree_climat = result.merge(df_aemet, how='inner', on='fecha')
df_ree_climat_cons = df_ree_climat.merge(df_miconsumo, how='inner', on='fecha')
df_ree_climat_cons.to_csv(r'.\dataset_completo.csv', index=False)