# Funciones para cargar y preprocesar datos
import os
import PyPDF2

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

pdf_path = "data/AccionDePersonal.pdf"
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location = "./chrome_langchain_db"
add_documents = not os.path.exists(db_location)

if add_documents:
    documents = []
    ids = []

    # Leer texto del PDF
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        pdf_text = ""
        for page in reader.pages:
            pdf_text += page.extract_text() or ""
    # Crear un solo documento con el texto extraído
    document = Document(
        page_content=pdf_text,
        metadata={"source": pdf_path},
        id="0"
    )
    documents.append(document)
    ids.append("0")


vector_store = Chroma(
    collection_name="restaurant_reviews",
    persist_directory=db_location,
    embedding_function=embeddings
)

if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)

