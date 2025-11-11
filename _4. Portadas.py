import requests
import os
import csv
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

def descargar_portada(url):
    try:
        respuesta = requests.get(url)
        nombre_archivo = os.path.basename(urlparse(url).path)
        ruta_destino = os.path.join("3. Portadas", nombre_archivo)
        if not os.path.exists(ruta_destino):
            with open(ruta_destino, 'wb') as portada:
                portada.write(respuesta.content)
            print(f"Descargada: {nombre_archivo}")
    except Exception as e:
        print(str(e))

def descargar_portadas_desde_csv(archivo_csv):
    if not os.path.exists("3. Portadas"):
        os.makedirs("3. Portadas")
    urls = []
    with open(archivo_csv, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            urls.append(row['Portada'])
    with ThreadPoolExecutor(max_workers=32) as executor:
        executor.map(descargar_portada, urls)

descargar_portadas_desde_csv('5. Redactado.csv')
