import os
from pathlib import Path
import fitz  # PyMuPDF
import re
from typing import List, Dict
import datetime
import dateparser


# Fecha de modificación del archivo
def obtener_fecha_archivo(ruta_pdf: str) -> str:
    stat = Path(ruta_pdf).stat()
    fecha_mod = datetime.datetime.fromtimestamp(stat.st_mtime)
    return fecha_mod.strftime("%Y-%m-%d")

def extraer_fecha_desde_texto(texto: str) -> str:

    patrones = [
        r'fecha\s*[:\-–]\s*(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})',  # Fecha: 7 de abril de 2025
        r'fecha\s*del\s*incidente\s*[:\-–]\s*(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})',
        r'fecha\s*[:\-–]\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})',  # Fecha: 12/03/2024
        r'(\d{4}-\d{2}-\d{2})',  # ISO 2024-10-15
    ]

    for patron in patrones:
        match = re.search(patron, texto, flags=re.IGNORECASE)
        if match:
            fecha_str = match.group(1).strip()
            fecha = dateparser.parse(fecha_str, languages=['es'])
            if fecha:
                return fecha.strftime('%Y-%m-%d')
            else:
                print(f"No se pudo parsear '{fecha_str}'")
    return None


def extraer_texto_pdf(ruta_pdf: str) -> str:
    """
    Extrae el texto completo de un archivo PDF usando PyMuPDF.
    """
    doc = fitz.open(ruta_pdf)
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    return texto


def limpiar_texto(texto: str) -> str:
    """
    Limpia el texto removiendo saltos de línea excesivos y espacios duplicados.
    """
    texto = re.sub(r'\n+', '\n', texto)         # Quita líneas vacías
    texto = re.sub(r'\s+', ' ', texto)          # Unifica espacios
    texto = texto.strip()
    return texto


def dividir_en_chunks(texto: str, max_palabras: int = 150) -> List[str]:
    """
    Divide el texto en chunks de máximo `max_palabras` palabras.
    """
    palabras = texto.split()
    chunks = []
    for i in range(0, len(palabras), max_palabras):
        chunk = " ".join(palabras[i:i + max_palabras])
        chunks.append(chunk)
    return chunks

def generar_chunks_con_metadata(ruta_pdf: str, max_palabras: int = 150) -> List[Dict]:
    """
    Procesa un PDF: extrae, limpia, divide en chunks y agrega metadatos.
    """
    texto = extraer_texto_pdf(ruta_pdf)
    texto_limpio = limpiar_texto(texto)
    # Detectamos la fecha
    fecha_extraida = extraer_fecha_desde_texto(texto_limpio)
    fecha_archivo = obtener_fecha_archivo(ruta_pdf)
    fecha_final = fecha_extraida or fecha_archivo

    chunks = dividir_en_chunks(texto_limpio, max_palabras)
    nombre_archivo = Path(ruta_pdf).stem

    resultado = []
    for i, chunk in enumerate(chunks):
        resultado.append({
            "documento": nombre_archivo,
            "chunk": chunk,
            "posicion": i,
            "fecha": fecha_final
        })

    return resultado

# ========== PROCESAR TODOS LOS PDFs EN UNA CARPETA ==========

def procesar_directorio_pdf(ruta_directorio: str) -> List[Dict]:

    resultados = []
    for archivo in os.listdir(ruta_directorio):
        if archivo.endswith(".pdf"):
            ruta_pdf = os.path.join(ruta_directorio, archivo)
            print(f"Procesando {archivo}...")
            chunks = generar_chunks_con_metadata(ruta_pdf)
            resultados.extend(chunks)
    return resultados
