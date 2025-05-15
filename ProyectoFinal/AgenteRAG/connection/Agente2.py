import asyncio
import json
import os
import sys
import httpx
import re
import numpy as np
import torch
import torch.nn.functional as F  # Add this import at the top of your file


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Setup local path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ReadPDF import contenido

OLLAMA_URL = "http://localhost:11434/api/generate"
model_to_use = "llama3.2"

sentence_model = SentenceTransformer("all-MiniLM-L6-v2")

#======= agrego device management ======
device = 'mps' if torch.backends.mps.is_available() else 'cuda' if torch.cuda.is_available() else 'cpu'
sentence_model = sentence_model.to(device)
print(f"🔌 Sentence Transformer ejecutándose en: {device.upper()}")


# Llamada a Ollama
async def get_completion(prompt: str, model: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                },
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "").strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Error: no se pudo obtener respuesta del modelo."

# Construir dataset
def construir_dataset_enriquecido(contenido_dict):
    dataset = {}
    for nombre_pdf, paginas in contenido_dict.items():
        texto_completo = "\n".join(paginas.values())
        dataset[nombre_pdf] = {"contenido": texto_completo}
    return dataset

# TF-IDF
def filtrar_por_tfidf(pregunta, dataset, top_k=3):
    docs = list(dataset.items())
    nombres = [nombre for nombre, _ in docs]
    textos = [info["contenido"] for _, info in docs]
    corpus = textos + [pregunta]

    vectores = TfidfVectorizer().fit_transform(corpus)
    similitudes = cosine_similarity(vectores[-1], vectores[:-1])[0]
    top_indices = similitudes.argsort()[::-1][:top_k]
    return {nombres[i]: dataset[nombres[i]] for i in top_indices}


def filtrar_por_embedding(pregunta, dataset, top_k=3):
    docs = list(dataset.items())
    nombres = [nombre for nombre, _ in docs]
    textos = [info["contenido"] for _, info in docs]

    embeddings = sentence_model.encode(textos + [pregunta], convert_to_tensor=True)
    pregunta_emb = embeddings[-1].unsqueeze(0)
    doc_embs = embeddings[:-1]

    # Use PyTorch's cosine similarity
    similitudes = F.cosine_similarity(pregunta_emb, doc_embs)
    top_indices = torch.topk(similitudes, k=top_k).indices.tolist()

    return {nombres[i]: dataset[nombres[i]] for i in top_indices}

# Agente
async def preguntar_al_agente(pregunta, dataset, metodo="tfidf"):
    if metodo == "tfidf":
        print("🔍 Filtrando con TF-IDF...")
        dataset_filtrado = filtrar_por_tfidf(pregunta, dataset)
    elif metodo == "embedding":
        print("🔍 Filtrando con Sentence Transformers...")
        dataset_filtrado = filtrar_por_embedding(pregunta, dataset)
    elif metodo == "llmrag":
        print("📚 Usando todos los documentos sin filtrar (LLM-RAG).")
        dataset_filtrado = dataset
    else:
        print("⚠ Método no reconocido. Se usará todo el dataset.")
        dataset_filtrado = dataset

    if not dataset_filtrado:
        print("⚠ Fallback: usando todo el dataset.")
        dataset_filtrado = dataset

    contexto = "\n\n".join([f"{nombre}:\n{info['contenido']}" for nombre, info in dataset_filtrado.items()])
    prompt = f"""Responde solo con base en los siguientes documentos:\n\n{contexto}\n\nPregunta:\n{pregunta}"""
    return await get_completion(prompt, model_to_use)

# Principal
def main():
    dataset = construir_dataset_enriquecido(contenido)
    preguntas = [
        "¿Cómo se llama la empresa y cuál es el perjuicio ocasionado?",
        "¿Qué tipo de problema fue, cuál fue la causa del incidente?",
        "¿Quiénes son los involucrados, se conoce el nombre de quien reporta el incidente?",
        "¿Qué archivo describe las sanciones ocasionadas?",
        "¿Cuál es el orden cronológico de los documentos?"
    ]
    metodos = ["tfidf", "embedding", "llmrag"]

    for metodo in metodos:
        print(f"\n🧠 Método: {metodo.upper()}\n{'=' * 60}")
        for i, pregunta in enumerate(preguntas, 1):
            print(f"\n🔵 Pregunta {i}: {pregunta}")
            respuesta = asyncio.run(preguntar_al_agente(pregunta, dataset, metodo))
            print(f"🟢 Respuesta:\n{respuesta}\n{'─' * 80}")

if __name__ == "__main__":
    main()
