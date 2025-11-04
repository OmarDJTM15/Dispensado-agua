import csv
import os
from datetime import datetime
from utils.config import RUTA_CSV


def registrar_despacho(litros: float, monto: float):
    """Agrega un registro nuevo al CSV con fecha, litros y monto."""
    # Asegurarse de que exista el directorio
    os.makedirs(os.path.dirname(RUTA_CSV), exist_ok=True)

    # Crear archivo si no existe
    archivo_nuevo = not os.path.exists(RUTA_CSV)
    with open(RUTA_CSV, mode="a", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)
        if archivo_nuevo:
            writer.writerow(["fecha", "litros", "monto"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), litros, monto])
