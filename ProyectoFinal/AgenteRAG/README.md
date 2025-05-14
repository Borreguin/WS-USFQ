# AgenteRAG: Asistente virtual local con RAG y LLM (Ollama)

Estructura del proyecto:
- utils/data_loader.py: carga y preprocesa datos
- utils/pdf_parser.py: extracción de texto de PDFs
- retriever.py: búsqueda informada/no informada
- llm_interface.py: conexión con Ollama
- agent.py: orquestador
- main.py: interfaz de usuario

data/: tus archivos de datos
embeddings/: vectores generados (opcional)

Requisitos en requirements.txt


## Pasos realizados 

- Creacion de un ambiente virtua

``` 
python -m venv venv 
```

- Activar ambiente virtual

``` 
.\venv\Scripts\Activate 
```

- Instalar las dependencias dentro del ambiente: (requirements.txt)

- Instalar Ollama
    - Instalar un modelo: https://ollama.com/library
        - llama 3.2
        
    - Instalar unmodelo embebido (para los documentos pdf)
        - mxbai-embed-large

- Ejecutar app
```
python ./main.py
```