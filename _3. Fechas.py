import csv
from datetime import datetime, timedelta
import random

def articulos_por_dia(mes, semana):
    if mes <= 2:
        return (mes - 1) * 6 + semana * 2
    elif mes <= 4:
        return 24 + (mes - 3) * 4
    else:
        return 32

def leer_total_articulos_desde_csv(ruta_archivo):
    with open(ruta_archivo, mode='r', encoding='utf-8') as csvfile:
        lector = csv.reader(csvfile)
        next(lector)
        return sum(1 for fila in lector if any(fila))

def actualizar_csv_con_fechas_de_publicacion(ruta_archivo):
    total_articulos = leer_total_articulos_desde_csv(ruta_archivo)
    print(total_articulos)
    articulos_publicados = 0
    fecha_inicio = datetime(2024, 1, 1)
    fecha_actual = fecha_inicio
    fechas_publicacion = []
    while articulos_publicados < total_articulos:
        mes = (fecha_actual - fecha_inicio).days // 30 + 1
        semana = ((fecha_actual - fecha_inicio).days % 30) // 7 + 1
        articulos_diarios = articulos_por_dia(mes, semana)
        if total_articulos - articulos_publicados <= 0:
            articulos_diarios = 1
        for _ in range(articulos_diarios):
            if articulos_publicados < total_articulos:
                hora_aleatoria = random.randint(7, 22)
                minuto_aleatorio = random.randint(0, 59)
                segundo_aleatorio = random.randint(0, 59)
                tiempo_aleatorio = datetime(fecha_actual.year, fecha_actual.month, fecha_actual.day, hora_aleatoria, minuto_aleatorio, segundo_aleatorio)
                fechas_publicacion.append(tiempo_aleatorio.strftime("%Y-%m-%d %H:%M:%S"))
                articulos_publicados += 1
        fecha_actual += timedelta(days=1)
    with open(ruta_archivo, mode='r', encoding='utf-8') as csvfile:
        lector = csv.reader(csvfile)
        filas = list(lector)
    filas[0].append("Fecha")
    for i, fila in enumerate(filas[1:], start=1):
        fila.append(fechas_publicacion[i-1])
    with open(ruta_archivo, mode='w', newline='', encoding='utf-8') as csvfile:
        escritor = csv.writer(csvfile)
        escritor.writerows(filas)

ruta_archivo = "5. Redactado.csv"
actualizar_csv_con_fechas_de_publicacion(ruta_archivo)
