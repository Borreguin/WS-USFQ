import os
from pathlib import Path
import fitz  # PyMuPDF
import re
from typing import List, Dict
from datetime import datetime

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


def dividir_en_chunks(texto: str, max_palabras: int = 300) -> List[str]:
    """
    Divide el texto en chunks de máximo `max_palabras` palabras.
    """
    palabras = texto.split()
    chunks = []
    for i in range(0, len(palabras), max_palabras):
        chunk = " ".join(palabras[i:i + max_palabras])
        chunks.append(chunk)
    return chunks

def generar_chunks_con_metadata(ruta_pdf: str, max_palabras: int = 300) -> List[Dict]:
    """
    Procesa un PDF: extrae, limpia, divide en chunks y agrega metadatos.
    """
    texto = extraer_texto_pdf(ruta_pdf)
    texto_limpio = limpiar_texto(texto)
    chunks = dividir_en_chunks(texto_limpio, max_palabras)

    nombre_archivo = Path(ruta_pdf).stem
    fecha_procesamiento = datetime.now().strftime("%Y-%m-%d")

    resultado = []
    for i, chunk in enumerate(chunks):
        resultado.append({
            "documento": nombre_archivo,
            "chunk": chunk,
            "posicion": i,
            "fecha": fecha_procesamiento
        })
    return resultado

# ========== PROCESAR TODOS LOS PDFs EN UNA CARPETA ==========

def procesar_directorio_pdf(ruta_directorio: str) -> List[Dict]:
    """
    Recorre todos los PDFs en el directorio y genera los chunks con metadatos.
    """
    resultados = []
    for archivo in os.listdir(ruta_directorio):
        if archivo.endswith(".pdf"):
            ruta_pdf = os.path.join(ruta_directorio, archivo)
            print(f"Procesando {archivo}...")
            chunks = generar_chunks_con_metadata(ruta_pdf)
            resultados.extend(chunks)
    return resultados
