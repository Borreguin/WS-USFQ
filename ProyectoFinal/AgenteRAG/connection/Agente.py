import asyncio
import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import httpx
import re

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ReadPDF import contenido  # Usa tu lector ya existente
from keyandcontext import KeyAndContext  # Si ya lo estás usando



# Configuración de Ollama
OLLAMA_URL = "http://localhost:11434/api/generate"
model_to_use = "llama3.2"  # O el modelo que prefieras

async def get_completion(prompt: str, model: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:  # Aumenté el timeout
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False  # Importante para recibir respuesta completa
                },
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "").strip()
    except httpx.ConnectError:
        print("Error: No se puede conectar al servidor Ollama. ¿Está corriendo?")
        return "Error: Servidor Ollama no disponible."
    except Exception as e:
        print(f"Error detallado: {str(e)}")
        return "Error: no se pudo obtener respuesta del modelo."


def test():
    promptDisponible = "Estas disponible?"
    completion = asyncio.run(get_completion(promptDisponible, model_to_use))
    print(completion)

# Construir dataset enriquecido desde contenido
def construir_dataset_enriquecido(contenido_dict):
    dataset = {}
    for nombre_pdf, paginas in contenido_dict.items():
        texto_completo = "\n".join(paginas.values())
        dataset[nombre_pdf] = {
            "contenido": texto_completo,
            "fecha": None,
            "empresa": None,
            "perjuicio": None,
            "tipo": None,
            "causa": None,
            "sanciones": None,
            "involucrados": [],
            "reporta": None
        }
    return dataset


# Guardar el dataset en JSON
def guardar_dataset_json(dataset, ruta="dataset.json"):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

#Usamos dos algoritmos de búsqueda para mejorar el modelo

# 🔍 TF-IDF
def filtrar_por_tfidf(pregunta, dataset, top_k=3):
    documentos = list(dataset.items())
    nombres = [nombre for nombre, _ in documentos]
    textos = [info["contenido"] for _, info in documentos]
    corpus = textos + [pregunta]

    vectorizer = TfidfVectorizer()
    vectores = vectorizer.fit_transform(corpus)
    similitudes = cosine_similarity(vectores[-1], vectores[:-1])[0]

    top_indices = similitudes.argsort()[::-1][:top_k]
    return {nombres[i]: dataset[nombres[i]] for i in top_indices}

# 🔍 Jaccard
def jaccard_sim(str1, str2):
    set1 = set(re.findall(r'\w+', str1.lower()))
    set2 = set(re.findall(r'\w+', str2.lower()))
    return len(set1 & set2) / len(set1 | set2) if set1 | set2 else 0

def filtrar_por_jaccard(pregunta, dataset, umbral=0.05):
    resultados = {}
    for nombre, info in dataset.items():
        sim = jaccard_sim(pregunta, info["contenido"])
        if sim >= umbral:
            resultados[nombre] = info
    return resultados

# Usar Ollama para responder una pregunta sobre el dataset
async def preguntar_al_agente(pregunta: str, dataset: dict, metodo: str = "jaccard"):
    # Selección dinámica del método
    if metodo == "tfidf":
        print("🔍 Filtrando con TF-IDF...")
        dataset_filtrado = filtrar_por_tfidf(pregunta, dataset)
    elif metodo == "jaccard":
        print("🔍 Filtrando con Jaccard...")
        dataset_filtrado = filtrar_por_jaccard(pregunta, dataset)
    else:
        print("⚠Método desconocido, usando todo el dataset.")
        dataset_filtrado = dataset

    if not dataset_filtrado:
        print("⚠No se encontraron documentos relevantes, usando todo el dataset.")
        dataset_filtrado = dataset

    contexto = "\n\n".join([f"{nombre}:\n{info['contenido']}" for nombre, info in dataset_filtrado.items()])
    prompt = f"""
    Responde solo con base en los siguientes documentos:
        
    {contexto}
        
    Pregunta:
    {pregunta}
        """
    respuesta = await get_completion(prompt, model_to_use)
    #print(respuesta)
    return respuesta
    # return await get_completion(prompt, model_to_use)



# Ejecución principal
# def main():
#     # Paso 1: Construir dataset desde contenido PDF
#     dataset = construir_dataset_enriquecido(contenido)
#
#     # Paso 2: Guardarlo si deseas conservarlo para otros scripts
#     guardar_dataset_json(dataset)
#
#     # Paso 3: Ejemplo de pregunta al agente
#     pregunta = "¿Cuál es el orden cronológico de los documentos?"
#     metodo = "jaccard"  # Poner "jaccard" para probar otro algoritmo
#
#     # Paso 4: Ejecutar consulta
#     respuesta = asyncio.run(preguntar_al_agente(pregunta, dataset, metodo))
#     print(f"\n Pregunta: {pregunta}\n Respuesta:\n{respuesta}")

def main():
    # Construir dataset
    dataset = construir_dataset_enriquecido(contenido)
    guardar_dataset_json(dataset)

    # Lista de preguntas a evaluar
    preguntas = [
        "¿Cómo se llama la empresa y cuál es el perjuicio ocasionado?",
        "¿Qué tipo de problema fue, cuál fue la causa del incidente?",
        "¿Quiénes son los involucrados, se conoce el nombre de quien reporta el incidente?",
        "¿Qué archivo describe las sanciones ocasionadas?",
        "¿Cuáles son los documentos más relevantes sobre este caso?"
    ]

    for i, pregunta in enumerate(preguntas, 1):
        print(f"\n🔵 Pregunta {i}: {pregunta}")
        respuesta = asyncio.run(preguntar_al_agente(pregunta, dataset, "jaccard"))
        print(f"🟢 Respuesta:\n{respuesta}\n")
        print("─" * 80)  # Separador visual

if __name__ == "__main__":
    main()
    # test()